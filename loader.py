from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from utils.misc import logging 

from data import config

bot = Bot(config.API_TOKEN, validate_token=True)
storage = RedisStorage2(config.REDIS_HOST)
dp = Dispatcher(bot, storage=storage)
logging.setup()