from typing import Any

from starlette.concurrency import run_in_threadpool

from hurricaneapi.dependencies.models import Dependant


async def run_endpoint_function(
    *,
    dependant: Dependant,
    values: dict[str, Any],
    is_coroutine: bool,
) -> Any:
    assert dependant.call is not None, "Endpoint must be a function"
    if is_coroutine:
        return await dependant.call(**values)
    else:
        return await run_in_threadpool(dependant.call, **values)
