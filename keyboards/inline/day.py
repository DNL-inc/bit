from aiogram import types
from keyboards.inline import back_callback, blank_callback
from middlewares import _
from models.event import Day

keyboard = types.InlineKeyboardMarkup(row_width=1)
for day in Day:
    keyboard.add(types.InlineKeyboardButton(day.name, callback_data=day.name))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
