from aiogram.types.chat_member import ChatMemberLeft
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from bot.http_clients.drivex_client import send_subscribed_user_ack
from bot.constants.bot_settings import CHAT_ID_TEST
from bot.constants.texts import TEXT_IF_USER_SUBSCRIBED
from bot.bot_creater import logger

from datetime import datetime, timedelta
from pytz import utc
import asyncio
import json


async def _check_user_subscribe(bot, user_id) -> bool:
    await logger.debug("Run check_user_subscribe function!")

    user_status = await bot.get_chat_member(chat_id=CHAT_ID_TEST, user_id=user_id)  #5703225789)
    await logger.debug(type(user_status))
    if isinstance(user_status, ChatMemberLeft):
        return False
    else:
        return True


async def _subscribe_status_message_actioner(bot: Bot, user_id, check_number: str):
    await logger.debug("Running _subscribe_status_message_actioner")

    is_subscribed_user = await _check_user_subscribe(bot, user_id)
    if is_subscribed_user:
        asyncio.create_task(send_subscribed_user_ack(json.dumps({"user_id": user_id})))
        await bot.send_message(user_id, text=TEXT_IF_USER_SUBSCRIBED)

        await logger.info(f"CHECK RESULT: user with id:{user_id} is already subscribed!")
    else:
        await logger.info(f"CHECK RESULT: user with id:{user_id} isn't subscribed yet!")

        current_time = datetime.utcnow()
        if check_number == "FIRST":
            await _create_second_delayed_check(bot, user_id, current_time + timedelta(seconds=8))

        if check_number == "SECOND":
            await _create_third_delayed_check(bot, user_id, current_time + timedelta(seconds=13))

        if check_number == "THIRD":
            await logger.info("Finished all checks")


async def _create_third_delayed_check(bot: Bot, user_id, run_time):
    await logger.debug("Running third_delayed_check!")

    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(_subscribe_status_message_actioner, trigger='date', run_date=run_time,
                      kwargs={'bot': bot, 'user_id': user_id, 'check_number': "THIRD"})
    scheduler.start()


async def _create_second_delayed_check(bot: Bot, user_id, run_time):
    await logger.debug("Running second_delayed_check!")

    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(_subscribe_status_message_actioner, trigger='date', run_date=run_time,
                      kwargs={'bot': bot, 'user_id': user_id, 'check_number': "SECOND"})
    scheduler.start()


async def _create_first_delayed_check(bot: Bot, user_id, run_time):
    await logger.debug("Running first_delayed_check!")

    scheduler = AsyncIOScheduler(timezone=utc)
    scheduler.add_job(_subscribe_status_message_actioner, trigger='date', run_date=run_time,
                      kwargs={'bot': bot, 'user_id': user_id, 'check_number': "FIRST"})
    scheduler.start()


async def user_subscribe_actioner(bot, user_id):
    """
    Firstly - check user subscribe status.
    Secondly - create delayed_checks.
    """
    await logger.debug("Running subscribe_actioner")

    if await _check_user_subscribe(bot, user_id):  # If user already subscribed
        await logger.info(f"User with id: {user_id} is already subscribed")
        return

    current_time = datetime.utcnow()
    await _create_first_delayed_check(bot, user_id, current_time + timedelta(seconds=5))
