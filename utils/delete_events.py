import datetime

from aiogram import Bot

from data.config import LOCAL_TZ
from models import Event


async def delete(bot: Bot):
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = LOCAL_TZ.localize(
        datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day))
    events = await Event.filter(event_over=timestamp).all()
    for event in events:
        await event.delete()
