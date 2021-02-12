from aiogram import types
from models import Subgroup, User
from middlewares import _
from keyboards.inline import blank_callback, back_callback


async def get_keyboard(group_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    subgroups = await Subgroup().select_subgroups_in_group(group_id)
    if subgroups:
        for subgroup in subgroups:
            keyboard.add(types.InlineKeyboardButton(subgroup.title, callback_data='subgroup-'+str(subgroup.id)))
    else:
        keyboard.add(types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='subgroup')))
    keyboard.add(types.InlineKeyboardButton('Добавить', callback_data='add-subgroup'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard