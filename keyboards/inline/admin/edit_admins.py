from aiogram import types

from keyboards.inline import back_callback

keyboard = types.InlineKeyboardMarkup(1)
keyboard.add(types.InlineKeyboardButton("Или ты хочешь отнять силу у кого-то?", callback_data="edit-admins"))
keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
