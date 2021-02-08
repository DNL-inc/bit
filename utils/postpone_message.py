import datetime
from typing import List

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked

from data.config import LOCAL_TZ
from models import PostponeMessage, Admin, User, Group



async def send_postpone_messages(bot: Bot):
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = LOCAL_TZ.localize(
        datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour,
                          timestamp_now.minute))
    messages = await PostponeMessage.filter(sending_time=timestamp).all()
    for message in messages:
        admin = await Admin.get(id=message.creator_id)
        users: List[User]
        if admin.role.name == 'supreme':
            users = await get_users(all=True)
        elif admin.role.name == 'improved':
            users = await get_users(faculty=admin.faculty_id)
        else:
            users = await get_users(group=admin.group_id)
        for user in users:
            try:
                await bot.send_message(user.tele_id, message.text)
            except BotBlocked:
                pass
        await message.delete()


async def get_users(faculty=None, group=None, all=False):
    if all:
        return await User().select_all_users()
    elif group:
        return await User.filter(group=group).all()
    else:
        groups = await Group.filter(faculty=faculty).all()
        users = list()
        for group in groups:
            users += await User.filter(group=group).all()
        return users
