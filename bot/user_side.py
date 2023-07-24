from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

from constans import BOT_TOKEN

from deep_linking_hanler import deep_linking_handler

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

btn_1 = InlineKeyboardButton('Community', url="https://youtube.com")
btn_2 = InlineKeyboardButton("Support", url="https://google.com")
keyboard = InlineKeyboardMarkup().add(btn_1).add(btn_2)


async def extract_referral_code(encoded_string):
    """
    Проверяет наличие данных, переданных вместе с командой.
    Возвращает закодированную строку с данными, если они есть.
    """
    string_parts = encoded_string.split()
    return string_parts[1] if len(string_parts) > 1 else None


@dp.message_handler(commands=['start', ])
async def start(message: types.Message):
    print(message.text)
    user_id = message.from_user.id
    username = message.from_user.username

    encoded_payload = await extract_referral_code(message.text)  # Split string and give payload string
    if encoded_payload:
        await deep_linking_handler(encoded_payload, user_id, username)

    await bot.send_message(message.chat.id, text=f"Привет, {username}", reply_markup=keyboard)
