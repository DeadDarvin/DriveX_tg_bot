from bot.constans import CHAT_ID_TEST
from aiogram.types.chat_member import ChatMemberLeft
from bot.bot_creater import logger
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from pytz import utc

IS_SUBSCRIBE = False


async def _check_user_subscribe_status(bot, user_id) -> bool:
    await logger.debug("Run check_subscribe function!")

    user_status = await bot.get_chat_member(chat_id=CHAT_ID_TEST, user_id=user_id)  #5703225789)
    await logger.debug(type(user_status))
    if isinstance(user_status, ChatMemberLeft):
        return False
    else:
        return True


async def _subscribe_status_message_actioner(bot: Bot, user_id):
    await logger.debug("Running _subscribe_actioner")

    global IS_SUBSCRIBE
    if IS_SUBSCRIBE:
        return

    is_subscribed_user = await _check_user_subscribe_status(bot, user_id)
    if is_subscribed_user:
        await bot.send_message(user_id, text="Опа, красавец. Подписан!")
        IS_SUBSCRIBE = True
        await logger.info(f"USER {user_id} subscribed!")
    else:
        await logger.info(f"USER {user_id} didn't subscribe!")


async def _create_delayed_check(bot: Bot, user_id, run_time):
    await logger.debug("Running _add_timer")

    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(_subscribe_status_message_actioner, trigger='date', run_date=run_time,
                      kwargs={'bot': bot, 'user_id': user_id})
    scheduler.start()


async def user_subscribe_actioner(bot, user_id):
    await logger.debug("Running subscribe_actioner")
    current_time = datetime.utcnow()
    await _create_delayed_check(bot, user_id, current_time + timedelta(seconds=5))
    await _create_delayed_check(bot, user_id, current_time + timedelta(seconds=8))
    await _create_delayed_check(bot, user_id, current_time + timedelta(seconds=13))
    await logger.debug("HI")

