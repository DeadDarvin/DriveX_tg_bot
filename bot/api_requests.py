import json
from aiohttp import ClientSession
import asyncio
from functools import wraps


def create_session(function):
    @wraps(function)
    async def wrapper(*args, **kwargs):
        async with ClientSession() as session:
            await function(session, *args, **kwargs)
    return wrapper


async def _request(session: ClientSession, user_data: json):
    async with session.post("http://localhost:8080/", data=user_data) as response:
        status_code = response.status
        print(status_code)
        good_code = False
        if response.status == 200:
            good_code = True
        return good_code, await response.json()


@create_session
async def send_user_tg_to_api(session: ClientSession, user_data: json):
    while True:
        good_code, response = await _request(session, user_data)
        if good_code:
            break
        else:
            await asyncio.sleep(3)
