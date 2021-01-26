from aiogram import types
from keyboards.inline import back_callback, blank_callback

keyboard = types.InlineKeyboardMarkup(row_width=1)
keyboard.add(types.InlineKeyboardButton("Скоро будет доступно", callback_data=blank_callback.new(category='blank')))
keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
