from typing import Callable, Any, Optional
from hurricaneapi.routing.router import Router
from hurricaneapi.responses.response import Response


class HurricaneApi:

    def __init__(self, version: str = '0.1.0', project_name: str = 'HurricaneAPI project'):
        self.version = version
        self.project_name = project_name
        self.router: Router = Router()

    def get(self, path: str) -> Callable[..., Any]:
        return self.router.get(path=path)

    def post(self, path: str) -> Callable[..., Any]:
        return self.router.post(path=path)

    async def _call_async_endpoint(self, async_func: Callable[..., Any], scope, receive, send):
        result: Optional[Any | Response] = await async_func()
        if isinstance(result, Response):
            await result.__call__(scope=scope, receive=receive, send=send)
        else:
            await Response(content=result).__call__(scope=scope, receive=receive, send=send)

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        if scope['path'] in self.router.route_list and scope['method'] in self.router.route_list[scope['path']]:
            await self._call_async_endpoint(
                async_func=self.router.route_list[scope['path']][scope['method']].endpoint,
                scope=scope,
                receive=receive,
                send=send,
            )


