from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsChat(BoundFilter):
    async def check(self, msg: types.Message):
        try:
            msg.chat.type
        except AttributeError:
            return msg.message.chat.type in ['supergroup', 'group']
        else:
            return msg.chat.type in ['supergroup', 'group']
