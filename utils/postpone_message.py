
import datetime
from typing import List

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, ChatNotFound

from data.config import LOCAL_TZ
from models import PostponeMessage, Admin, User, Group, Chat


async def send_postpone_messages(bot: Bot):
    timestamp_now = LOCAL_TZ.localize(datetime.datetime.now())
    timestamp = LOCAL_TZ.localize(
        datetime.datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day, timestamp_now.hour,
                          timestamp_now.minute))
    messages = await PostponeMessage.filter(sending_time=timestamp).all()
    for message in messages:
        admin = await Admin.get(id=message.creator_id)
        users: List[User]
        chats: List[Chat]
        if admin.role.name == 'supreme':
            users = await get_users(all=True)
            chats = await get_chats(all=True)
        elif admin.role.name == 'improved':
            users = await get_users(faculty=admin.faculty_id)
            chats = await get_chats(faculty=admin.faculty_id)
        else:
            users = await get_users(group=admin.group_id)
            chats = await get_chats(group=admin.group_id)
        for user in users:
            try:
                msg = await bot.send_message(user.tele_id, message.text)
                await bot.pin_chat_message(user.tele_id, msg.message_id)
            except:
                pass

        for chat in chats:
            try:
                msg = await bot.send_message(chat.tele_id, message.text)
                await bot.pin_chat_message(chat.tele_id, msg.message_id)
            except:
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


async def get_chats(faculty=None, group=None, all=None):
    if all:
        return await Chat.all()
    elif group:
        return await Chat.filter(group=group).all()
    else:
        groups = await Group.filter(faculty=faculty).all()
        chats = list()
        for group in groups:
            chats += await Chat.filter(group=group).all()
        return chats
