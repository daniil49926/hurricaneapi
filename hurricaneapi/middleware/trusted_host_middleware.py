from typing import Optional, Sequence

from hurricaneapi.middleware import BaseMiddleware
from hurricaneapi.responses import PlainTextResponse, Response


class TrustedHostMiddleware(BaseMiddleware):

    def __init__(
        self,
        allowed_hosts: Optional[list[str]] = None,
    ):
        if allowed_hosts is None:
            self.allowed_hosts = ['*']
        elif isinstance(allowed_hosts, Sequence):
            self.allowed_hosts = list(allowed_hosts)
        else:
            raise RuntimeError('Allowed hosts must be sequence')

    async def run_logic(self, *args, **kwargs) -> Response | None:
        if len(self.allowed_hosts) == 1 and self.allowed_hosts[0] == '*':
            return

        host = kwargs.get('scope', {}).get('client')[0]
        if host in self.allowed_hosts:
            return

        return PlainTextResponse("Invalid host header", status_code=400)


