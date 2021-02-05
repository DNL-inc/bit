from aiogram import types
from datetime import datetime

from tortoise.timezone import localtime

from data.config import LOCAL_TZ
from models import Admin, User, PostponeMessage
from keyboards.inline import blank_callback, back_callback



async def get_keyboard(admin: Admin):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    messages = await PostponeMessage().select_messages_by_creator(admin.id)
    if messages:
        for message in messages:
            sending_time = localtime(message.sending_time, LOCAL_TZ.zone)
            keyboard.add(types.InlineKeyboardButton("На " + sending_time.strftime("%d.%m.%Y %H:%M") + " " + message.text[:10] + "...", callback_data='msg-'+str(message.id)))
    else:
        keyboard.add(types.InlineKeyboardButton("Нет тут ничего", callback_data=blank_callback.new(category='settings')))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='send_msg')))
    return keyboard