from typing import Callable, Any
from hurricaneapi.routing.Router import Router


class HurricaneApi:

    def __init__(self, version: str = '0.1.0', project_name: str = 'HurricaneAPI project'):
        self.version = version
        self.project_name = project_name
        self.router: Router = Router()

    def get(self, path: str) -> Callable[..., Any]:
        return self.router.get(path=path)

    def post(self, path: str) -> Callable[..., Any]:
        return self.router.post(path=path)

    async def _call_async_endpoint(self, async_func: Callable[..., Any], send):
        result = await async_func()
        await self.send_message_with_status_200(result, send)

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        if scope['path'] in self.router.route_list and scope['method'] in self.router.route_list[scope['path']]:
            await self._call_async_endpoint(
                async_func=self.router.route_list[scope['path']][scope['method']].endpoint,
                send=send,
            )
        else:
            await self.send_message_with_status_404(send=send)

    @staticmethod
    async def send_message_with_status_200(message: bytes, send):
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': message,
        })

    @staticmethod
    async def send_message_with_status_404(send):
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': b'Page not found',
        })
