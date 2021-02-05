import datetime

from data.config import LOCAL_TZ
from models import PostponeMessage


async def send_postpone_messages():
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = LOCAL_TZ.localize(datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour, timestamp_now.minute))
    messages = await PostponeMessage.filter(sending_time=timestamp).all()
    print(messages)