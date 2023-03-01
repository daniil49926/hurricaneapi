import json
from typing import Any, Optional, Mapping
from hurricaneapi.responses.response import Response


class JSONResponse(Response):
    def __init__(
        self,
        content: Any = None,
        media_type: Optional[str] = None,
        charset: Optional[str] = 'utf-8',
        status_code: int = 200,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None
    ) -> None:
        super().__init__(content, media_type, charset, status_code, headers)
        self.media_type = 'application/json'

    @staticmethod
    def render_response(content: Any) -> bytes:
        return json.dumps(content).encode('utf-8')
