from aiogram import types
from models import Subgroup, User
from middlewares import _
from keyboards.inline import blank_callback, back_callback


async def get_keyboard(group_id, user_subgroups):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    subgroups = await Subgroup().select_subgroups_in_group(group_id)
    if subgroups:
        if user_subgroups: user_subgroups = [subgroup.id for subgroup in user_subgroups]
        for subgroup in subgroups:
            if user_subgroups and subgroup.id in user_subgroups:
                keyboard.add(types.InlineKeyboardButton("✔️"+subgroup.title, callback_data='subgroup-'+str(subgroup.id)))
            else:
                keyboard.add(types.InlineKeyboardButton(subgroup.title, callback_data='subgroup-'+str(subgroup.id)))
    else:
        keyboard.add(types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='subgroup')))

    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='group')))
    keyboard.add(types.InlineKeyboardButton(_('Продолжить'), callback_data='complete'))
    return keyboard