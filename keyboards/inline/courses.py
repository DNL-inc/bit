from data import config
from aiogram import types
from keyboards.inline import back_callback

keyboard = types.InlineKeyboardMarkup()
for course in range(1, config.NUMBER_COURSES+1):
    keyboard.add(types.InlineKeyboardButton(str(course)+'-курс', callback_data="course-"+str(course)))
keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='faculty')))