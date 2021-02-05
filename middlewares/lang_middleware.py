from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiogram import types
from models import User
from typing import Tuple, Any

async def get_lang(tele_id):
    user = await User().select_user_by_tele_id(tele_id)
    if user:
        return user.lang if user.lang else False


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user = types.User.get_current()
        return await get_lang(user.id) or user.language_code
