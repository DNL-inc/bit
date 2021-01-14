from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.misc import rate_limit
from models.user import User
from states.auth import AuthStates
from keyboards.inline.languages import keyboard


@rate_limit(10, 'start')
@dp.message_handler(CommandStart(), state='*')
async def start(msg: types.Message):
    await msg.answer("Привет!")
    user = await User().create_user(tele_id=msg.from_user.id, firstname=msg.from_user.first_name, lastname=msg.from_user.last_name, username=msg.from_user.username)
    if user:
        await msg.answer("Выбери язык: ", reply_markup=keyboard)
        await AuthStates.choose_lang.set()
        await msg.delete()
    else:
        await msg.delete()
        await msg.answer("Я тебя знаю!") 