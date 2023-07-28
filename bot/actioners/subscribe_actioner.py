from aiogram.types.chat_member import ChatMemberLeft
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from bot.http_clients.drivex_client import send_subscribed_user_ack
from bot.constants.texts import TEXT_IF_USER_SUBSCRIBED, TEXT_IF_USER_NOT_SUBSCRIBED
from bot.constants.keyboards import IM_SUBSCRIBE_BUTTON
from bot.constants.bot_settings import CHANEL_ID
from bot.bot_creater import logger

from datetime import datetime, timedelta
from pytz import utc
import asyncio


check_time_delays = {
    2: 6, 3: 6, 4: 6, 5: 9, 6: 3, 7: 60, 8: 60, 9: 60, 10: 60,
    11: 300, 12: 300, 13: 300, 14: 300, 15: 300, 16: 300, 17: 300, 18: 300, 19: 300, 20: 300
}


async def check_user_subscribe(bot, user_id) -> bool:
    await logger.debug("Run check_user_subscribe function!")

    user_status = await bot.get_chat_member(chat_id=CHANEL_ID, user_id=user_id)  # -1001905613285
    await logger.debug(type(user_status))
    if isinstance(user_status, ChatMemberLeft):
        return False
    else:
        return True


async def _create_delayed_check(bot: Bot, user_id, check_number: int, run_time):
    """ Создает таймер """
    await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::CREATION_DELAYED_CHECK!")

    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(subscribe_status_message_actioner, trigger='date', run_date=run_time,
                      kwargs={'bot': bot, 'user_id': user_id, 'check_number': check_number})
    scheduler.start()


async def subscribe_status_message_actioner(bot: Bot, user_id, check_number: int = 1):
    """
    General actioner for creation delayed_examinations.
    Check user subscribe status. Function create next delayed_examination if user is not subscribed yed.
    Send keyboard to user after 10 examination. Examinations will stop if user subscribe.
    Or examination number is 20.
    """
    await logger.info(f"{datetime.now()}:::USER_ID:{user_id}:::START {check_number} EXAMINATION!")

    if check_number == 6:  # Last check
        return
    if check_number == 4:
        await bot.send_message(user_id, text=TEXT_IF_USER_NOT_SUBSCRIBED, reply_markup=IM_SUBSCRIBE_BUTTON)

    #  Directly check
    is_subscribed_user = await check_user_subscribe(bot, user_id)
    if is_subscribed_user:
        asyncio.create_task(send_subscribed_user_ack({"user_id": user_id}))
        await bot.send_message(user_id, text=TEXT_IF_USER_SUBSCRIBED)

        await logger.info(f"CHECK RESULT: user with id:{user_id} is already subscribed!")
    else:
        await logger.info(f"CHECK RESULT: user with id:{user_id} isn't subscribed yet!")

        current_time = datetime.utcnow()
        current_delay = check_time_delays[check_number+1]
        next_check_time = current_time + timedelta(seconds=current_delay)
        await _create_delayed_check(bot, user_id, check_number+1, next_check_time)
