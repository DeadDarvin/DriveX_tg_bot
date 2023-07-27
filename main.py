from aiogram import executor

from bot.constants.bot_settings import BOT_DEBUG
from bot.constants.bot_settings import WEBHOOK_URL, WEBHOOK_PATH
from bot.constants.bot_settings import WEBAPP_HOST, WEBAPP_PORT

from bot.handlers import bot, dp
from bot.bot_creater import logger


async def on_startup(dp):
    await logger.info("WEBHOOK-START!")
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
