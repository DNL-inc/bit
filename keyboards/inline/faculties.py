from aiogram import types
from models import Faculty
from keyboards.inline import blank_callback, back_callback
from middlewares import _


async def get_keyboard(editable=False, one_faculty=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    faculties = await Faculty().select_all_faculties()
    if one_faculty:
        keyboard.add(types.InlineKeyboardButton(one_faculty.title, callback_data='faculty-'+str(one_faculty.id)))
    else:
        for faculty in faculties:
            keyboard.add(types.InlineKeyboardButton(faculty.title, callback_data='faculty-'+str(faculty.id)))
        if not faculties:
            keyboard.add(types.InlineKeyboardButton(_('Нет тут ничего'), callback_data=blank_callback.new(category='faculty')))
    if editable:
        keyboard.add(types.InlineKeyboardButton(_('Добавить'), callback_data='add-faculty'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard