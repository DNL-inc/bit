from aiogram import types
from models import Group
from data import config
from middlewares import _

from keyboards.inline import blank_callback, back_callback


async def get_keyboard(with_chat_settings: bool):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    settings = config.SETTIGS
    if settings:
        for key, value in settings.items():
            if not with_chat_settings and value == config.SETTIGS.get('chat-settings'):
                keyboard.add(types.InlineKeyboardButton("Удалить", callback_data='delete-chat'))
                continue
            keyboard.add(types.InlineKeyboardButton(value, callback_data=key))
    else:
        keyboard.add(
            types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='settings')))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='menu')))
    return keyboard
