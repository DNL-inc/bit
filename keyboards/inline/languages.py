from data import config
from aiogram import types

keyboard = types.InlineKeyboardMarkup(row_width=1)
for key, lang in config.LANGUAGES.items():
    keyboard.add(types.InlineKeyboardButton(lang, callback_data=key))        