from aiogram import types

from models import User

from keyboards.inline import back_callback

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton('15 минут', callback_data='notify-15'))
keyboard.add(types.InlineKeyboardButton('10 минут', callback_data='notify-10'))
keyboard.add(types.InlineKeyboardButton('5 минут', callback_data='notify-5'))
keyboard.add(types.InlineKeyboardButton('Во время начала события', callback_data='notify-0'))
keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='cancel')))
