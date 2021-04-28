from aiogram import types

from data.config import OPERATIONTS_EVENT
from keyboards.inline import back_callback, blank_callback
from middlewares import _

keyboard = types.InlineKeyboardMarkup(row_width=1)
for key, value in OPERATIONTS_EVENT.items():
    keyboard.add(types.InlineKeyboardButton(value, callback_data=key))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='event')))
