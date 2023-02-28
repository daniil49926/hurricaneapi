from typing import Dict, Callable, Any
from hurricaneapi.routing.Route import Route


class Router:

    def __init__(self):
        self.route_list: Dict[str, Dict[str, Route]] = {}

    def _add_route(
        self,
        path: str,
        method: str,
        endpoint_route: Route
    ) -> None:
        if path in self.route_list:
            self.route_list[path][method] = endpoint_route
        else:
            self.route_list[path] = {method: endpoint_route}

    def get(self, path: str) -> Callable[..., Any]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            route: Route = Route(path=path, method='GET', endpoint=func)
            self._add_route(path=path, method='GET', endpoint_route=route)
            return func
        return wrapper

    def post(self, path: str) -> Callable[..., Any]:
        def wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
            route: Route = Route(path=path, method='POST', endpoint=func)
            self._add_route(path=path, method='POST', endpoint_route=route)
            return func
        return wrapper
