from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from models.admin import Admin


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin
    
    async def check(self, msg: types.Message):
        tele_id = msg.from_user.id
        admin = await Admin().select_admin_by_tele_id(tele_id)
        return True if admin else False