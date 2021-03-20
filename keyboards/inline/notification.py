from aiogram import types

from keyboards.inline import back_callback
from models import User


async def get_keyboard(user, chat=False) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if user.notification:
        keyboard.add(types.InlineKeyboardButton("Выключить", callback_data='notification-trigger'))
        keyboard.add(types.InlineKeyboardButton('Время оповещения', callback_data='time-notification'))
        if not chat:
            keyboard.add(types.InlineKeyboardButton('Редактировать уведомления', callback_data='notifications'))
    else:
        keyboard.add(types.InlineKeyboardButton("Включить", callback_data='notification-trigger'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='settings')))
    return keyboard
