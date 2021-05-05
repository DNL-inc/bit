from aiogram import types
from keyboards.inline import back_callback, blank_callback
from middlewares import _
from models.event import Day

days = {
    'monday': _('Понедельник'),
    'tuesday': _('Вторник'),
    'wednesday': _('Среда'),
    'thursday': _('Четверг'),
    'friday': _('Пятница'),
    'saturday': _('Суббота'),
    'sunday': _('Воскресенье')
}

keyboard = types.InlineKeyboardMarkup(row_width=1)
for day_key, day in days.items():
    keyboard.add(types.InlineKeyboardButton(day, callback_data=day_key))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
