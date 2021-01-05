from aiogram import Dispatcher
from filters import isAdmin

def setup(dp: Dispatcher):
    dp.filters_factory.bind(isAdmin.IsAdminFilter)