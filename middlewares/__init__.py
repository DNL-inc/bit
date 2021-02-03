from aiogram import Dispatcher
from loader import dp

from .throttling import ThrottlingMiddleware
from .current_user import CurrentUserMiddleware
from .current_admin import CurrentAdminMiddleware


if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(CurrentUserMiddleware())
    dp.middleware.setup(CurrentAdminMiddleware())