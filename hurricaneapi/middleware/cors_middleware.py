from typing import Optional

from hurricaneapi.middleware import BaseMiddleware
from hurricaneapi.responses import PlainTextResponse, Response


class CORSMiddleware(BaseMiddleware):

    ALL_METHODS = ("DELETE", "GET", "HEAD", "PATCH", "POST", "PUT")
    SAFELISTED_HEADERS = {"Accept", "Accept-Language", "Content-Language", "Content-Type"}

    def __init__(
        self,
        allow_origins: Optional[list[str]] = None,
        allow_methods: Optional[list[str]] = None,
        allow_headers: Optional[list[str]] = None,
    ):

        if allow_methods is None or '*' in allow_methods:
            allow_methods = self.ALL_METHODS
        if allow_origins is None:
            allow_origins = ['*']
        if allow_headers is None:
            allow_headers = ['*']

        allow_all_origins = "*" in allow_origins
        allow_all_headers = "*" in allow_headers


        allow_headers = sorted(self.SAFELISTED_HEADERS | set(allow_headers))

        self.allow_origins = allow_origins
        self.allow_methods = allow_methods
        self.allow_headers = [h.lower() for h in allow_headers]
        self.allow_all_origins = allow_all_origins
        self.allow_all_headers = allow_all_headers


    async def run_logic(self, *args, **kwargs) -> Response | None :
        scope = kwargs.get('scope')
        method = scope.get('method')
        headers = scope.get('headers')
        failures = []
        if method not in self.allow_methods:
            failures.append("method")
        if not self.allow_all_headers:
            for i_headers in headers:
                if i_headers[0].decode('utf-8') not in self.allow_headers:
                    failures.append("headers")
                    break

        if failures:
            failure_text = "Disallowed CORS " + ", ".join(failures)
            return PlainTextResponse(failure_text, status_code=400)
