from aiogram import types
from keyboards.inline import back_callback
from middlewares import _

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton(_('Отмена'), callback_data=back_callback.new(category='cancel')))
