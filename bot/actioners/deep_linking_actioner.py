from bot.http_clients.drivex_client import send_user_tg_to_api
from bot.bot_creater import logger
from typing import Optional
import base64
import re
from datetime import datetime


async def _decode_payload_data(encoded_param_value: str) -> str:
    """ Декодирует данные. Возвращает сырую раскодированную строку """
    encoded_to_bytes = encoded_param_value.encode("ascii")
    decoded_from_bytes = base64.b64decode(encoded_to_bytes)
    decoded_param_value = decoded_from_bytes.decode("ascii")

    return decoded_param_value


async def _email_handler(decoded_email: str, user_data: dict):
    """ Handle request to api and getting user_info """
    user_data["email"] = decoded_email
    await logger.info(f"USER_WITH_EMAIL_DATA: {user_data}")
    await send_user_tg_to_api(user_data)


async def _is_valid_parameter_key(param_string) -> Optional[str]:
    logger.debug("Checking param_key")
    key = re.search("^.*_", param_string)
    if key is None:
        return
    return key.group()


async def _get_parameter_value(param_string):
    value = re.sub(r"^.*_", "", param_string)
    return value


async def deep_linking_handler(encoded_payload: str, user_data: dict):
    """ Определеят логику, зависящую от param_key """
    param_key = await _is_valid_parameter_key(encoded_payload)  # Example: e_
    if param_key is None:
        await logger.warning(f"{datetime.now()}:::USER:{user_data}:::INVALID_KEY!")
        return

    param_value = await _get_parameter_value(encoded_payload)  # Example: W2NoZXwucnVdCg

    try:
        decoded_payload = await _decode_payload_data(param_value)
        if param_key == "e_":  # Email
            await _email_handler(decoded_payload, user_data)
    except ValueError as err:
        await logger.warning(f"{datetime.now()}:::USER:{user_data}:::"
                             f"Attempt to hack: Correct key, but incorrect value: {err}")

