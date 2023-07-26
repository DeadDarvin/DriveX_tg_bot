import asyncio
from aiohttp import ClientSession
from functools import wraps


def create_session(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        async with ClientSession() as session:
            await function(session, *args, **kwargs)
    return wrapper


def retry_until_success(attempts: int):
    """
    Run function until success or attempts finished.
    Make 3 seconds pause between try.
    """
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            for try_ in range(attempts):
                success = await function(*args, **kwargs)
                if success:
                    break
                else:
                    await asyncio.sleep(3)
        return wrapper
    return decorator

