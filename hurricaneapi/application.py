from collections import deque
from typing import Any, Callable, Optional

from hurricaneapi.middleware import (
    BaseMiddleware,
    CORSMiddleware,
    TrustedHostMiddleware,
)
from hurricaneapi.responses.response import Response
from hurricaneapi.routing.router import Router


class HurricaneApi:

    def __init__(self, version: str = '0.1.0', project_name: str = 'HurricaneAPI project'):
        self.version = version
        self.project_name = project_name
        self.router: Router = Router()
        self.middleware_stack: deque = deque()
        self._build_base_middleware_in_stack()

    def get(self, path: str) -> Callable[..., Any]:
        return self.router.get(path=path)

    def post(self, path: str) -> Callable[..., Any]:
        return self.router.post(path=path)

    @staticmethod
    async def _call_async_endpoint(async_func: Callable[..., Any], scope, receive, send):
        result: Optional[Any | Response] = await async_func()
        if isinstance(result, Response):
            await result.__call__(scope=scope, receive=receive, send=send)
        else:
            await Response(content=result).__call__(scope=scope, receive=receive, send=send)

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        for stack_idx in range(len(self.middleware_stack) - 1, -1, -1):
            resp = await self.middleware_stack[stack_idx](scope, receive, send)
            if isinstance(resp, Response):
                await resp.__call__(scope=scope, receive=receive, send=send)
                return
        if scope['path'] in self.router.route_list and scope['method'] in self.router.route_list[scope['path']]:
            await self._call_async_endpoint(
                async_func=self.router.route_list[scope['path']][scope['method']].endpoint,
                scope=scope,
                receive=receive,
                send=send,
            )
        else:
            await Response(content="Not found", status_code=404).__call__(scope, receive, send)

    def add_middleware(self, middleware: list[BaseMiddleware]) -> None:
        self._build_user_middleware_in_stack(middleware)


    def _build_user_middleware_in_stack(
        self, user_middleware_list: Optional[list[BaseMiddleware]]
    ) -> None:

        for elm in user_middleware_list:
            if not isinstance(elm, BaseMiddleware):
                raise RuntimeError(
                    f'{elm} is not middleware.\n'
                    f'The correct middleware should be a subclass of BaseMiddleware'
                )
            for idx, base_middleware in enumerate(self.middleware_stack):
                if base_middleware.__class__ == elm.__class__:
                    self.middleware_stack[idx] = elm
                    break
            else:
                self.middleware_stack.appendleft(elm)

    def _build_base_middleware_in_stack(self) -> None:
        self.middleware_stack.append(CORSMiddleware())
        self.middleware_stack.append(TrustedHostMiddleware())
