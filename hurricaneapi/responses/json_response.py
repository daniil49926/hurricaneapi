import json
from typing import Any, Mapping, Optional

from hurricaneapi.responses.response import Response


class JSONResponse(Response):
    def __init__(
        self,
        content: Any = None,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None,
        status_code: int = 200,
    ) -> None:
        super().__init__(content=content, status_code=status_code, media_type='application/json', headers=headers)

    @staticmethod
    def render_response(content: Any) -> bytes:
        return json.dumps(content).encode('utf-8')
