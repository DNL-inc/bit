from aiogram import executor, Dispatcher

from loader import dp
import middlewares
import filters
import handlers
from utils.db_api import  create_db
from data import config


async def on_startup(dp: Dispatcher):
    await create_db()


if __name__ == "__main__":
    executor.start_polling(
        dp, skip_updates=config.SKIP_UPDATES, on_startup=on_startup)
