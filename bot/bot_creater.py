from aiogram import Bot
from aiogram import Dispatcher
from constans import BOT_TOKEN
from aiologger import Logger


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

logger = Logger.with_default_handlers(level="DEBUG")
