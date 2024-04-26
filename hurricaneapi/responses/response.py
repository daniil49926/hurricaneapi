from typing import Any, List, Mapping, Optional


class Response:
    def __init__(
        self,
        content: Any = None,
        media_type: Optional[str] = None,
        charset: Optional[str] = 'utf-8',
        status_code: int = 200,
        headers: Optional[Mapping[bytes | str, bytes | str]] = None
    ) -> None:
        self.media_type = media_type
        self.charset = charset
        self.status_code = status_code
        self.body = self.render_response(content=content)
        self.headers = self.initialization_headers(init_headers=headers)

    def initialization_headers(
        self,
        init_headers: Optional[Mapping[bytes | str, bytes | str]]
    ) -> List[tuple[bytes, bytes]]:
        headers_has_content_length: bool = False
        headers_has_content_type: bool = False
        if init_headers:
            bytes_headers = [
                (key.lower().encode('utf-8'), value.lower().encode('utf-8'))
                if isinstance(key, str) and isinstance(value, str)
                else (key.lower(), value.lower())
                for key, value in init_headers.items()
            ]
            headers_has_content_length = b'content-length' in [item[0] for item in bytes_headers]
            headers_has_content_type = b'content-type' in [item[0] for item in bytes_headers]
        else:
            bytes_headers = []

        if not headers_has_content_length:
            bytes_headers.append((b'content-length', str(len(self.body)).encode('utf-8')))

        if not headers_has_content_type:
            bytes_headers.append((b'content-type', str(self.media_type).encode('utf-8')))

        return bytes_headers

    @staticmethod
    def render_response(content: Any) -> bytes:
        if content is None:
            return b''
        if isinstance(content, bytes):
            return content
        return content.encode("utf-8")

    async def __call__(self, scope, receive, send):
        await send(
            {
                'type': 'http.response.start',
                'status': self.status_code,
                'headers': self.headers,
            }
        )
        await send(
            {
                'type': 'http.response.body',
                'body': self.body,
            }
        )
