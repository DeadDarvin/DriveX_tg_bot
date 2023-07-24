import json
from aiohttp import ClientSession


async def send_user_tg_to_api(user_email, user_id, username):
    user_json = json.dumps({
        "user_email": user_email,
        "user_id": user_id,
        "username": username
        }
    )

    async with ClientSession() as session:
        async with session.post("http://localhost:8080/", data=user_json) as response:
            return await response.json()
