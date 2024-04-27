
class BaseMiddleware:

    async def run_logic(self, *args, **kwargs) -> None:
        raise NotImplementedError

    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        return await self.run_logic(scope=scope, receive=receive, send=send)
