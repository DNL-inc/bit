from data import config
from aiogram import types
from keyboards.inline import back_callback
from middlewares import _

keyboard = types.InlineKeyboardMarkup(row_width=1)
for key, lang in config.LANGUAGES.items():
    keyboard.add(types.InlineKeyboardButton(lang, callback_data=key))

async def get_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key, lang in config.LANGUAGES.items():
        keyboard.add(types.InlineKeyboardButton(lang, callback_data=key))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard
