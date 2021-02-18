from aiogram import types

from keyboards.inline import blank_callback, back_callback
from middlewares import _
from models import Event


async def get_keyboard(day, group_id=None, editable=False, subgroup_id=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    events = None
    if subgroup_id:
        events = await Event.filter(subgroup=subgroup_id, day=day).all()
    elif group_id:
        events = await Event.filter(group=group_id, day=day).all()
    for event in events:
        keyboard.add(types.InlineKeyboardButton(event.title, callback_data='event-' + str(event.id)))
    if not events:
        keyboard.add(
            types.InlineKeyboardButton(_('Нет тут ничего'), callback_data=blank_callback.new(category='event')))
    if editable:
        keyboard.add(types.InlineKeyboardButton('Добавить', callback_data='add-event'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='subgroup')))
    return keyboard
