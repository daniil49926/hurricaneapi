from typing import Callable, Any, MutableMapping, Awaitable
from starlette.applications import Starlette
from hurricaneapi.routing.HurricaneRouter import HurricaneRouter


class HurricaneApi(Starlette):

    def __init__(
        self,
        version: str = "0.1.0",
    ) -> None:
        super().__init__()
        self.version = version
        self.router = HurricaneRouter()

    def get(
        self,
        path: str,
    ) -> Callable[..., Any]:
        return self.router.get(path)

    def post(
        self,
        path: str,
    ) -> Callable:
        return self.router.post(path)

    async def __call__(
        self,
        scope: MutableMapping[str, Any],
        receive: Callable[[], Awaitable[MutableMapping[str, Any]]],
        send: Callable[[MutableMapping[str, Any]], Awaitable[None]]
    ) -> None:
        await super().__call__(scope, receive, send)
