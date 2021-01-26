from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc import rate_limit, get_current_user
from keyboards.inline import blank_callback, back_callback
from states.menu import MenuStates
from keyboards.default import menu
from models import User



#should be down
@dp.message_handler(state="*")
async def unknown_msg(msg: types.Message, state: FSMContext):
    state = await state.get_state()
    text = f"""
{msg.from_user.full_name}, ты что-то делаешь не так.
Эхо в состоянии <code>{state}</code>"""
    await msg.answer(text)


@dp.callback_query_handler(state="*")
async def unknown_call(msg: types.CallbackQuery, state: FSMContext):
    state = await state.get_state()
    text = f"""
{msg.from_user.full_name}, ты что-то делаешь не так.
Эхо в состоянии <code>{state}</code>"""
    await msg.answer(text)
