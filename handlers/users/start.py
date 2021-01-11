from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.misc import rate_limit
from models.user import User


@rate_limit(10, 'start')
@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer("Привет!")