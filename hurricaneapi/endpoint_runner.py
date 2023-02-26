from typing import Any

from hurricaneapi.concurrency import non_blocking_sync_endpoint
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
        return await non_blocking_sync_endpoint(dependant.call, values)
