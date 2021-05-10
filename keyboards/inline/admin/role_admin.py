from aiogram import types

from keyboards.inline import back_callback
from models import Admin
from models.admin import Role


async def get_keyboard(admin: Admin):
    keyboard = types.InlineKeyboardMarkup(1)
    if admin.role.name == "supreme":
        for role in [i.name for i in Role]:
            if role != "supreme":
                keyboard.add(types.InlineKeyboardButton(role.capitalize(), callback_data=role))
    elif admin.role.name == "improved":
        for role in [i.name for i in Role]:
            if role == "ordinary":
                keyboard.add(types.InlineKeyboardButton(role.capitalize(), callback_data=role))

    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
    return keyboard
