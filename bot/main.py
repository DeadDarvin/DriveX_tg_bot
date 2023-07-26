from aiogram import executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from constants.bot_settings import BOT_DEBUG, WEBHOOK_URL, WEBAPP_PORT, WEBAPP_HOST, WEBHOOK_PATH
from bot.handlers import bot, dp
from bot.bot_creater import logger


async def on_startup(dp):
    await logger.info()
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    await logger.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    await logger.warning('Bye!')


if __name__ == '__main__':
    if BOT_DEBUG:
        executor.start_polling(dp, skip_updates=True)
    else:
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
