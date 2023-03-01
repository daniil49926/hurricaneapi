from typing import Any, Optional, Mapping
from hurricaneapi.responses.response import Response


class PlainTextResponse(Response):
    def __init__(
        self,
        content: Any = None,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None
    ) -> None:
        super().__init__(content=content, media_type="text/plain", headers=headers)
