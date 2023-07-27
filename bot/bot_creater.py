from aiogram import Bot
from aiogram import Dispatcher
from bot.constants.bot_settings import BOT_TOKEN
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

handler = AsyncFileHandler("bot.log")
logger = Logger.with_default_handlers(level="DEBUG")
logger.add_handler(handler)
