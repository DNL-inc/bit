from aiogram import types
from keyboards.inline import back_callback
from middlewares import _


keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton(_('Удалить'), callback_data='delete-msg'))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='delete_msg')))
