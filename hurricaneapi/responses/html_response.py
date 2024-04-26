from typing import Any, Mapping, Optional

from hurricaneapi.responses.response import Response


class HTMLResponse(Response):
    def __init__(
        self,
        content: Any = None,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None
    ) -> None:
        super().__init__(content=content, media_type="text/html", headers=headers)
