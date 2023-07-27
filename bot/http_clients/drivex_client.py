import json
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError
from bot.constants.http_settings import PAUSE_BETWEEN_REQUESTS
from bot.bot_creater import logger
from bot.constants.http_settings import USER_DATA_ATTEMPTS, SUBSCRIBE_ACK_ATTEMPTS
from bot.constants.http_settings import USER_DATA_ENDPOINT, SUBSCRIBE_ACK_ENDPOINT
from bot.constants.bot_settings import API_KEY
from .decorators import retry_until_success, create_session


async def _request(session: ClientSession, url: str, user_data: json):
    headers = {"API_KEY": API_KEY}
    async with session.post(url, json=user_data, ssl=False, headers=headers) as response:
        good_code = False
        await logger.info(f"REQUEST: user_data={user_data}\n"
                          f"status_code={response.status}, response={await response.text()}")
        if response.status == 200:
            good_code = True
        return good_code


@create_session
@retry_until_success(attempts=USER_DATA_ATTEMPTS, pause=PAUSE_BETWEEN_REQUESTS)
async def send_user_tg_to_api(session: ClientSession, user_data: json):
    await logger.debug(user_data)
    await logger.debug(type(user_data))
    try:
        is_completed = await _request(session, USER_DATA_ENDPOINT, user_data)
        return is_completed
    except ClientError as err:
        await logger.error(f"ERROR IN USER DATA SENDING REQUEST: {err}")
        return False


@create_session
@retry_until_success(attempts=SUBSCRIBE_ACK_ATTEMPTS, pause=PAUSE_BETWEEN_REQUESTS)
async def send_subscribed_user_ack(session: ClientSession, user_data: json):
    await logger.debug(user_data)
    try:
        status_code = await _request(session, SUBSCRIBE_ACK_ENDPOINT, user_data)
        return status_code
    except ClientError as err:
        await logger.error(f"ERROR IN SUBSCRIBE ACKNOWLEDGMENT REQUEST: {err}")
        return False
