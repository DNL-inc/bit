from aiogram import types
from keyboards.inline import back_callback, delete_callback
from models import Faculty


async def get_keyboard(category):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Удалить', callback_data=delete_callback.new(category=category)))
    keyboard.add(types.InlineKeyboardButton('Отмена', callback_data=back_callback.new(category='cancel')))
    return keyboard
