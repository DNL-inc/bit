from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsPrivate(BoundFilter):
    async def check(self, msg: types.Message):
        try:
            msg.chat.type
        except AttributeError:
            return msg.message.chat.type == 'private'
        else:
            return msg.chat.type == 'private'
