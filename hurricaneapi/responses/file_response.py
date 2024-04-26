import asyncio
import hashlib
import os
from email.utils import formatdate
from mimetypes import guess_type
from typing import Mapping, Optional
from urllib.parse import quote

import aiofiles

from hurricaneapi.responses.response import Response


class FileResponse(Response):

    def __init__(
        self,
        path_to_file: str,
        status_code: int = 200,
        headers: Optional[Mapping[str, str]] = None,
        filename: Optional[str] = None,
    ) -> None:
        self.path_to_file = path_to_file
        self.filename = filename
        super().__init__(
            status_code=status_code,
            headers=headers,
            media_type=guess_type(filename or self.path_to_file)[0] or "text/plain",
        )

        if self.filename:
            q_filename = quote(self.filename)
            meta_name = (
                f"attachment; filename*=utf-8''{q_filename}"
                if q_filename != self.filename
                else
                f'attachment; filename="{self.filename}"'
            )
            self.headers.append((b'content-disposition', meta_name.encode('utf-8')))


    async def __call__(self, scope, receive, send) -> None:
        try:
            stat_result = await asyncio.to_thread(os.stat, self.path_to_file)
        except FileNotFoundError as error:
            raise RuntimeError(f"File {self.path_to_file} not exist.") from error
        for idx, header in enumerate(self.headers):
            if header[0] == b'content-length':
                self.headers.pop(idx)
                break
        self.headers.append(
            (
                b'content-length',
                str(stat_result.st_size).encode('utf-8')
            )
        )
        self.headers.append(
            (
                b'last-modified',
                formatdate(stat_result.st_mtime, usegmt=True).encode('utf-8')
            )
        )
        self.headers.append(
            (
                b'etag',
                hashlib.md5(
                    (str(stat_result.st_mtime) + "-" + str(stat_result.st_size)).encode()
                ).hexdigest().encode('utf-8')
            )
        )

        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.headers,
            }
        )
        async with aiofiles.open(self.path_to_file, mode="rb") as file:
            while chunk := await file.read(64 * 1024):
                if len(chunk) <= 0:
                    break
                await send(
                    {
                        "type": "http.response.body",
                        "body": chunk,
                        "more_body": True,
                    }
                )
