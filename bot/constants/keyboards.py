from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

# keyboard for /start-message
btn_1 = InlineKeyboardButton('Community', url="https://t.me/InterCity_app")
btn_2 = InlineKeyboardButton("Support", url="https://t.me/InterCitySupport")
START_KEYBOARD = InlineKeyboardMarkup().add(btn_1).add(btn_2)


subscribe_btn = InlineKeyboardButton("Я подписан!", callback_data="subscribe")
IM_SUBSCRIBE_BUTTON = InlineKeyboardMarkup().add(subscribe_btn)
