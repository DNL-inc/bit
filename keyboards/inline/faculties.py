from aiogram import types
from models import Faculty
from keyboards.inline import blank_callback, back_callback

async def get_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    faculties = await Faculty().select_all_faculties()
    for faculty in faculties:
        keyboard.add(types.InlineKeyboardButton(faculty.title, callback_data='faculty-'+str(faculty.id)))
    if not faculties:
        keyboard.add(types.InlineKeyboardButton('Нет тут ничего', callback_data=blank_callback.new(category='faculty')))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
    return keyboard