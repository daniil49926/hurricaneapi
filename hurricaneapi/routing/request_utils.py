import asyncio
from typing import Callable, Coroutine, Any

from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from hurricaneapi.endpoint_runner import run_endpoint_function
from hurricaneapi.dependencies.models import Dependant
from hurricaneapi.dependencies.utils import solve_dependencies


def get_request_handler(
    dependant: Dependant,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    is_coroutine: bool = asyncio.iscoroutinefunction(dependant.call)

    async def app(request: Request) -> Response:
        body = None
        if dependant.body_params:
            body = await request.json()
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=body
        )
        values, errors = solved_result
        if errors:
            raise ValidationError(errors=errors)

        raw_response = await run_endpoint_function(
            dependant=dependant, values=values, is_coroutine=is_coroutine
        )
        if isinstance(raw_response, Response):
            return raw_response
        if isinstance(raw_response, (dict, str, int, float, type(None))):
            return JSONResponse(raw_response)
        else:
            raise Exception("Type of response is not supported")
    return app
