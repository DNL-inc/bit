import datetime
from typing import List
import calendar

import pytz
from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked

from data.config import LOCAL_TZ
from models import Admin, User, Group, Event, Notification, Chat
from middlewares import _


async def send(bot: Bot):
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = datetime.datetime(1991, 8, 24, timestamp_now.hour,
                                  timestamp_now.minute)

    users = await User().select_all_users()
    for user in users:
        user_delta = datetime.timedelta(minutes=user.notification_time)
        notifications = await Notification.filter(user=user.id).all()
        for notification in notifications:
            await notification.fetch_related("event")
            event = await Event.filter(id=notification.event.id, time=timestamp + user_delta,
                                       day=calendar.day_name[timestamp_now.weekday()].lower()).first()
            if event:
                try:
                    await bot.send_message(user.tele_id, _(
                        "Осталось {} минут до события [{}]({})!".format(user.notification_time, event.title,
                                                                        event.link)),
                                           parse_mode="Markdown", disable_web_page_preview=True)
                except:
                    pass

    chats = await Chat.filter(notification=True).all()
    for chat in chats:
        chat_delta = datetime.timedelta(minutes=chat.notification_time)
        await chat.fetch_related("group")

        events = await Event.filter(group=chat.group,
                                    day=calendar.day_name[timestamp_now.weekday()].lower()).all()

        for event in events:
            time = event.time.replace(tzinfo=None)
            if timestamp + chat_delta == time:
                try:
                    msg = await bot.send_message(chat.tele_id,
                                                 _("Осталось {} минут до события [{}]({})!".format(
                                                     user.notification_time,
                                                     event.title, event.link)),
                                                 parse_mode="Markdown", disable_web_page_preview=True)
                    await bot.pin_chat_message(chat.tele_id, msg.message_id)
                except:
                    pass
