from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class IsChat(BoundFilter):
    async def check(self, msg: types.Message):
        return msg.chat.type in ['supergroup', 'group']
