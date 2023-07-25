from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.bot_creater import bot, dp
from bot.actioners.deep_linking_actioner import deep_linking_handler
from bot.actioners.subscribe_actioner import user_subscribe_actioner
from bot.api_requests import send_user_tg_to_api

from typing import Optional
import json
from bot.bot_creater import logger


# keyboard for /start-message
btn_1 = InlineKeyboardButton('Community', url="https://t.me/InterCity_app")
btn_2 = InlineKeyboardButton("Support", url="https://t.me/InterCitySupport")
keyboard = InlineKeyboardMarkup().add(btn_1).add(btn_2)


async def _extract_referral_code(encoded_string):
    """
    Проверяет наличие данных, переданных вместе с командой.
    Возвращает закодированную строку с данными, если они есть.
    """
    string_parts = encoded_string.split()
    return string_parts[1] if len(string_parts) > 1 else None


async def _form_user_data_from_message(user_id: int, username: Optional[str]) -> dict:
    user_data = {"user_id": user_id}
    if username:
        user_data["username"] = username

    return user_data


@dp.message_handler(commands=['start', ])
async def start(message: types.Message):
    """
    Check deep-linking. Send user_data to api-driveX.
    Send message with keyboard to user.
    """
    await logger.debug("Run start-handler!")
    user_id = message.from_user.id
    username = message.from_user.username

    user_data: dict = await _form_user_data_from_message(user_id, username)

    encoded_payload = await _extract_referral_code(message.text)  # Split string and give payload string
    if encoded_payload:
        await deep_linking_handler(encoded_payload, user_data)
    else:
        await send_user_tg_to_api(json.dumps(user_data))

    await user_subscribe_actioner(bot, user_id)

    await bot.send_message(user_id, text=f"Привет, {username}", reply_markup=keyboard)


@dp.message_handler(commands=['test', ])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Done")

# @dp.message_handler()
# async def get_chat_id(message: types.Message):
#     print(message.text)
#     chat_id = message.chat.id
#     await bot.send_message(1338248618, text=f"Это чат айди: {chat_id}")
