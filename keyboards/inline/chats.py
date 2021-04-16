from aiogram import types

from middlewares import _
from keyboards.inline import blank_callback, back_callback
from models import Chat


async def get_keyboard(user_id, editable=False):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    chats = await Chat.filter(creator_id=user_id).all()
    if chats:
        for chat in chats:
            keyboard.add(types.InlineKeyboardButton(chat.title, callback_data='chat-' + str(chat.id)))
    else:
        keyboard.add(
            types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='chat')))
    if editable:
        keyboard.add(types.InlineKeyboardButton(_('➕ Добавить ➕'), callback_data='add-chat'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard
