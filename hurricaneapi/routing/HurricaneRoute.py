from typing import Callable, Any
from starlette.routing import Route, request_response
from hurricaneapi.dependencies.utils import get_dependant
from hurricaneapi.routing.request_utils import get_request_handler


class HurricaneRoute(Route):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        method: str,
    ):
        self.path = path
        self.endpoint = endpoint
        self.method = method
        assert callable(endpoint), "The end point of the hurricane must be called"
        self.dependant = get_dependant(path=self.path, call=self.endpoint)
        self.app = request_response(get_request_handler(dependant=self.dependant))
        super().__init__(
            path=self.path,
            endpoint=self.endpoint
        )
