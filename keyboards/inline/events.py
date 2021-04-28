from aiogram import types

from data import config
from keyboards.inline import blank_callback, back_callback
from middlewares import _
from models import Event, Notification


async def get_keyboard(day, group_id=None, editable=False, subgroup_id=None, notify=False, user=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    events = list()

    if subgroup_id and isinstance(subgroup_id, list):
        for sub_id in subgroup_id:
            if (sub_id.group_id == group_id):
                events += await Event.filter(subgroup=sub_id.id, day=day).all()

        group_events = await Event.filter(group=group_id, day=day).all()
        for event in group_events:
            if event in events: continue
            events.append(event)

    else:
        if group_id and not subgroup_id:
            events = await Event.filter(group=group_id, day=day).all()
        elif subgroup_id:
            events = await Event.filter(subgroup=subgroup_id, day=day).all()

    for event in events:
        title = event.title if len(event.title) < 15 else event.title[:15] + "..."
        if notify:
            if await Notification.filter(user=user.id, event=event.id).first():
                keyboard.add(
                    types.InlineKeyboardButton(
                        "✅" + config.TYPE_EVENT.get(event.type) + " " + title,
                        callback_data='event-' + str(event.id)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton(
                        config.TYPE_EVENT.get(event.type) + " " + title,
                        callback_data='event-' + str(event.id)))
        else:
            keyboard.add(
                types.InlineKeyboardButton(
                    config.TYPE_EVENT.get(event.type) + " " + title,
                    callback_data='event-' + str(event.id)))
    if not events:
        keyboard.add(
            types.InlineKeyboardButton(_('Нет тут ничего'), callback_data=blank_callback.new(category='event')))
    if editable:
        keyboard.add(types.InlineKeyboardButton(_('Добавить'), callback_data='add-event'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='subgroup')))
    return keyboard
