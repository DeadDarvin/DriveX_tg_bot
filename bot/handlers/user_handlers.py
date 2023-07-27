from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from bot.bot_creater import bot, dp
from bot.actioners.deep_linking_actioner import deep_linking_handler
from bot.actioners.subscribe_actioner import user_subscribe_actioner
from bot.http_clients.drivex_client import send_user_tg_to_api
from bot.constants.texts import START_TEXT, START_IMAGE_URL
from bot.constants.bot_settings import ADMIN_ID
from bot.bot_creater import logger

from typing import Optional
import json
import asyncio

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
        asyncio.create_task(deep_linking_handler(encoded_payload, user_data))  # Will be payload-handle
    else:
        asyncio.create_task(send_user_tg_to_api(json.dumps(user_data)))  # Send without payload

    asyncio.create_task(user_subscribe_actioner(bot, user_id))  # Check subscribe and creation checks

    await bot.send_photo(
        chat_id=user_id,
        photo=START_IMAGE_URL,
        caption=START_TEXT,
        reply_markup=keyboard
    )


@dp.message_handler(commands=['team_test_focus', ])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, "Done")


@dp.message_handler(content_types=['new_chat_members', ])
async def get_chat_id(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(ADMIN_ID, text=f"Айди нашего чата: {chat_id}")
