import datetime
from typing import List

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked

from data.config import LOCAL_TZ
from models import Admin, User, Group, Event


async def delete(bot: Bot):
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = LOCAL_TZ.localize(
        datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day))
    events = await Event.filter(event_over=timestamp).all()
    for event in events:
        await event.delete()
