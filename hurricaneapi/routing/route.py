from typing import Any, Callable


class Route:
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        method: str
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.method = method
        assert callable(endpoint), "An hurricane endpoint must be a callable"
