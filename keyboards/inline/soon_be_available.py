from aiogram import types
from keyboards.inline import back_callback, blank_callback
from middlewares import _

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton(_("Когда-то.. здесь обязательно что-то будет"), callback_data=blank_callback.new(category='blank')))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
