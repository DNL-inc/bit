from aiogram import types

from loader import dp
from utils.misc import rate_limit
from keyboards.inline import blank_callback


@rate_limit(10, 'blank')
@dp.callback_query_handler(text_contains='blank', state="*")
async def blank_calls(call: types.CallbackQuery):
    await call.answer(cache_time=60, text='Хватит жать - остановись')


@dp.message_handler(state="*")
async def unknown_msg(message: types.Message):
    text = f"{message.from_user.full_name}, ты что-то делаешь не так."
    await message.answer(text)

@dp.callback_query_handler(state="*")
async def unknown_call(message: types.CallbackQuery):
    text = f"{message.from_user.full_name}, ты что-то делаешь не так."
    await message.answer(text)
