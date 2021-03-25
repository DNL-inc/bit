from aiogram import types

from data.config import LOCAL_TZ
from models import Admin, User, PostponeMessage
from keyboards.inline import blank_callback, back_callback


async def get_keyboard(admin: Admin):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    admins = None
    if admin.role.name == 'supreme':
        admins = await Admin.all()
    elif admin.role.name == 'improved':
        admins = await Admin.filter(role="ordinary", faculty=admin.faculty_id).all()
    if admins:
        for a in admins:
            await a.fetch_related("group")
            keyboard.add(types.InlineKeyboardButton(a.group.title, callback_data='admin-' + str(a.id)))
    else:
        keyboard.add(
            types.InlineKeyboardButton("Нет тут ничего", callback_data=blank_callback.new(category='blank')))
    keyboard.add(types.InlineKeyboardButton('Добавить нового', callback_data="add-admin"))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
    return keyboard
