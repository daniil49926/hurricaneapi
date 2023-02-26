from starlette.routing import Router
from hurricaneapi.routing.HurricaneRoute import HurricaneRoute
from typing import Callable, Any


class HurricaneRouter(Router):
    def __init__(self) -> None:
        super().__init__()
        self.route_class = HurricaneRoute

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        method: str,
    ):
        self.routes.append(
            self.route_class(
                path=path,
                endpoint=endpoint,
                method=method,
            )
        )

    def get(
        self,
        path: str
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: [Callable[..., Any]]) -> [Callable[..., Any]]:
            self.add_api_route(path=path, endpoint=func, method="get")
            return func
        return wrapper

    def post(
        self,
        path: str,
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def wrapper(func: [Callable[..., Any]]) -> [Callable[..., Any]]:
            self.add_api_route(path=path, endpoint=func, method="post")
            return func
        return wrapper
