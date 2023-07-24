import base64
import re
from api_requests import send_user_tg_to_api


async def _decode_payload_data(encoded_param_value: str) -> str:
    """ Декодирует данные. Возвращает сырую раскодированную строку """
    encoded_to_bytes = encoded_param_value.encode("ascii")
    decoded_from_bytes = base64.b64decode(encoded_to_bytes)
    decoded_param_value = decoded_from_bytes.decode("ascii")

    print(decoded_param_value)
    return decoded_param_value


async def _get_parameter_from_link(param_string: str) -> tuple[str, str]:
    key = re.search("^.*_", param_string).group()  # Example-key: e_
    value = re.sub(r"^.*_", "", param_string)  # Example-value: W2NoZXRreXBhY2FuQG1haWwucnVdCg==
    return key, value


async def _email_handler(decoded_email: str, user_id, username):
    """ Handle request to api and getting user_info """
    print(decoded_email)
    response = await send_user_tg_to_api(decoded_email, user_id, username)
    print(response)


async def deep_linking_handler(encoded_payload: str, user_id, username):
    """ Определеят логику, зависящую от param_key """
    param_key, param_value = await _get_parameter_from_link(encoded_payload)  # Example: key=e_, value=W2NoZXwucnVdCg
    decoded_payload = await _decode_payload_data(param_value)

    if param_key == "e_":  # Email
        await _email_handler(decoded_payload, user_id, username)
