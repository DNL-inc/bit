from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from data import config
from utils.misc import logging
from utils.db_api import create_db, close_db


logging.setup()


async def on_startup(dp: Dispatcher):
    import filters, middlewares
    from handlers import error, user
    filters.setup(dp)
    user.setup(dp)
    error.setup(dp)
    middlewares.setup(dp)
    await create_db()


async def on_shutdown(dp: Dispatcher):
    await storage.close()
    # await close_db()

if __name__ == "__main__":
    bot = Bot(config.API_TOKEN, validate_token=True)
    storage = RedisStorage2(config.REDIS_HOST)
    dp = Dispatcher(bot, storage=storage)
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup, on_shutdown=on_shutdown)
