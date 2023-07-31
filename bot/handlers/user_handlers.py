from aiogram import types
from bot.bot_creater import bot, dp
from bot.actioners.deep_linking_actioner import deep_linking_handler
from bot.actioners.subscribe_actioner import subscribe_status_message_actioner
from bot.http_clients.drivex_client import send_user_tg_to_api
from bot.http_clients.drivex_client import send_subscribed_user_ack
from bot.constants.texts import START_TEXT, START_IMAGE_URL, TEXT_IF_USER_SUBSCRIBED
from bot.constants.keyboards import START_KEYBOARD, COMEBACK_BUTTON
from bot.bot_creater import logger
from bot.actioners.subscribe_actioner import check_user_subscribe
from typing import Optional
import asyncio
from datetime import datetime


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
    Delegate creation of delayed examination if user is not subscribed.
    Send message with keyboard to user.
    """
    user_id = message.from_user.id
    username = message.from_user.username
    await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::START!")

    user_data: dict = await _form_user_data_from_message(user_id, username)

    encoded_payload = await _extract_referral_code(message.text)  # Split string and give payload string
    if encoded_payload:
        await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::WITH_PAYLOAD!")
        asyncio.create_task(deep_linking_handler(encoded_payload, user_data))  # Will be payload-handle
    else:
        await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::WITHOUT_PAYLOAD!")
        asyncio.create_task(send_user_tg_to_api(user_data))  # Send without payload

    is_subscribed = await check_user_subscribe(bot, user_id)
    if is_subscribed:
        asyncio.create_task(send_subscribed_user_ack({"user_id": user_id}))
    else:
        asyncio.create_task(subscribe_status_message_actioner(bot, user_id))  # Delegate creation of delayed checks

    await bot.send_photo(
        chat_id=user_id,
        photo=START_IMAGE_URL,
        caption=START_TEXT,
        reply_markup=START_KEYBOARD
    )


# @dp.message_handler(commands=['team_test_focus', ])
# async def start(message: types.Message):
#     await bot.send_message(message.chat.id, "Done")


@dp.callback_query_handler(text="subscribe")
async def check_user_is_subscribed(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::CLICK_SUBS_BUTTON!")

    is_subscribed = await check_user_subscribe(bot, user_id)
    if is_subscribed:
        asyncio.create_task(send_subscribed_user_ack({"user_id": user_id}))
        await bot.send_message(
            chat_id=user_id,
            text=TEXT_IF_USER_SUBSCRIBED,
            reply_markup=COMEBACK_BUTTON
        )
