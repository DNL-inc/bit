from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc import rate_limit, get_current_user
from keyboards.inline import blank_callback, back_callback
from states.menu import MenuStates
from keyboards.default import menu
from models import User


@rate_limit(10, 'blank')
@dp.callback_query_handler(text_contains='blank', state="*")
async def blank_calls(call: types.CallbackQuery):
    await call.answer(cache_time=60, text='Хватит жать - остановись')


#should be down
@dp.message_handler(state="*")
async def unknown_msg(msg: types.Message):
    text = f"{msg.from_user.full_name}, ты что-то делаешь не так."
    await msg.answer(text)


@dp.callback_query_handler(state="*")
async def unknown_call(msg: types.CallbackQuery):
    text = f"{msg.from_user.full_name}, ты что-то делаешь не так."
    await msg.answer(text)
