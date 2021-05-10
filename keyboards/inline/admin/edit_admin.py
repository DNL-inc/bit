from aiogram import types

from keyboards.inline import blank_callback, back_callback
from models import Admin


async def get_keyboard(admin: Admin, adminManager: Admin):
    keyboard = types.InlineKeyboardMarkup(1)
    if admin.role.name == "supreme":
        keyboard.add(types.InlineKeyboardButton("Только совет джедаев имеет право",
                                                callback_data=blank_callback.new(category='blank')))
    else:
        if adminManager.role.name == "supreme":
            keyboard.add(types.InlineKeyboardButton("Изменить Роль", callback_data="edit-role"))
            keyboard.add(types.InlineKeyboardButton("Изменить Факультет", callback_data="edit-faculty"))

        keyboard.add(types.InlineKeyboardButton("Изменить Группу", callback_data="edit-group"))
        keyboard.add(types.InlineKeyboardButton("Удалить", callback_data="delete-admin"))

    keyboard.add(types.InlineKeyboardButton("Назад", callback_data=back_callback.new(category='admins')))

    return keyboard
