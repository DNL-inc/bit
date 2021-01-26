from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from models import Admin

class IsAdmin(BoundFilter):
    async def check(self, msg: types.Message):
        return Admin().is_admin_exists(msg.from_user.id)
