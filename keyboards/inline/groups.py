from aiogram import types
from models import Group

from keyboards.inline import blank_callback, back_callback


async def get_keyboard(filters):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    groups = await Group().select_groups_by_filters(filters)
    if groups:
        for group in groups:
            keyboard.add(types.InlineKeyboardButton(group.title, callback_data='group-'+str(group.id)))
    else:
        keyboard.add(types.InlineKeyboardButton("Нет тут ничего", callback_data=blank_callback.new(category='group')))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='course')))
    return keyboard