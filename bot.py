from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from data import config
from utils.misc import logging

logging.setup()

if __name__ == "__main__":
    bot = Bot(config.API_TOKEN, validate_token=True)
    storage = RedisStorage2(config.REDIS_HOST)
    dp = Dispatcher(bot, storage=storage)
    executor.start_polling(dp, skip_updates=True)
