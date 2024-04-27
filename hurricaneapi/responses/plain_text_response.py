from typing import Any, Mapping, Optional

from hurricaneapi.responses.response import Response


class PlainTextResponse(Response):
    def __init__(
        self,
        content: Any = None,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None,
        status_code: int = 200,
    ) -> None:
        super().__init__(content=content, status_code=status_code, media_type="text/plain", headers=headers)
