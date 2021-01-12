from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.misc import logging 

from data import config

bot = Bot(config.API_TOKEN, validate_token=True)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.setup()