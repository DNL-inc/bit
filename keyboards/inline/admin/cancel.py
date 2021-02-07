from aiogram import types
from keyboards.inline import back_callback

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton('Отмена', callback_data=back_callback.new(category='cancel')))
