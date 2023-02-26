import functools

from anyio import to_thread
from typing import Callable, Any


async def non_blocking_sync_endpoint(
    func: Callable, key_val_args: dict[str, Any], *args,
) -> Callable:
    func = functools.partial(func, key_val_args)
    return await to_thread.run_sync(func=func, *args)
