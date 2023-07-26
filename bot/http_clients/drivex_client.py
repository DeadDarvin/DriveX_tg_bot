import json
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from bot.bot_creater import logger
from bot.constants import USER_DATA_ATTEMPTS, SUBSCRIBE_ACK_ATTEMPTS
from bot.constants import USER_DATA_ENDPOINT, SUBSCRIBE_ACK_ENDPOINT
from bot.constants import API_KEY
from .decorators import retry_until_success, create_session


async def _request(session: ClientSession, url: str, user_data: json):
    headers = {"API_KEY": API_KEY}
    print(user_data)
    async with session.post(url, data=user_data, ssl=False, headers=headers) as response:
        good_code = False
        print(response.status)
        print(await response.text())
        if response.status == 200:
            good_code = True
        return good_code


@retry_until_success(attempts=USER_DATA_ATTEMPTS)
@create_session
async def send_user_tg_to_api(session: ClientSession, user_data: json):
    try:
        status_code = await _request(session, USER_DATA_ENDPOINT, user_data)
        print(status_code)
        return status_code
    except ClientError as err:
        await logger.error(f"ERROR IN USER DATA SENDING REQUEST: {err}")
        return False


@retry_until_success(attempts=SUBSCRIBE_ACK_ATTEMPTS)
@create_session
async def send_subscribed_user_ack(session: ClientSession, user_data: json):
    try:
        status_code = await _request(session, SUBSCRIBE_ACK_ENDPOINT, user_data)
        return status_code
    except ClientError as err:
        await logger.error(f"ERROR IN SUBSCRIBE ACKNOWLEDGMENT REQUEST: {err}")
        return False
