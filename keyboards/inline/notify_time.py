from aiogram import types
from middlewares import _
from models import User

from keyboards.inline import back_callback

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton(_('15 минут'), callback_data='notify-15'))
keyboard.add(types.InlineKeyboardButton(_('10 минут'), callback_data='notify-10'))
keyboard.add(types.InlineKeyboardButton(_('5 минут'), callback_data='notify-5'))
keyboard.add(types.InlineKeyboardButton(_('В момент начала события'), callback_data='notify-0'))
keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='cancel')))
