from typing import Any, Optional, Mapping
from urllib.parse import quote

from hurricaneapi.responses.response import Response

class RedirectResponse(Response):
    def __init__(
        self,
        url: str,
        status_code: int = 307,
        content: Any = None,
        media_type: Optional[str] = None,
        charset: Optional[str] = 'utf-8',
        headers: Optional[Mapping[bytes | str, bytes | str]] = None
    ) -> None:
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            charset=charset,
        )
        if isinstance(url, str):
            self.headers.append((b'location', quote(url, safe=":/%#?=@[]!$&'()*+,;").encode('utf-8')))
        else:
            raise RuntimeError(
                f"{url=} {type(url)=} Redirect path is not valid. Use only str url for redirect."
            )