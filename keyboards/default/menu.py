from aiogram import types

from models.admin import Admin
from models.user import User
from data import config

async def get_keyboard(user: User):
    admin = await Admin().select_admin_by_user_id(user.id)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=1)
    [keyboard.add(types.KeyboardButton(page)) for page in config.MENU[:-1]]
    if admin:
        keyboard.add(types.KeyboardButton(config.MENU[-1]))
    return keyboard

