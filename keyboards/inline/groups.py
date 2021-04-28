from aiogram import types
from models import Group
from middlewares import _
from keyboards.inline import blank_callback, back_callback


async def get_keyboard(filters, editable=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    groups = await Group().select_groups_by_filters(filters)
    if groups:
        for group in groups:
            keyboard.add(types.InlineKeyboardButton(group.title, callback_data='group-'+str(group.id)))
    else:
        keyboard.add(types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='group')))
    if editable:
        keyboard.add(types.InlineKeyboardButton(_('Добавить'), callback_data='add-group'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='course')))
    return keyboard