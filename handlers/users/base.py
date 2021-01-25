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


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='menu'), state=MenuStates.all_states)
async def back_to_menu(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.message.delete()
    await MenuStates.mediate.set()
    keyboard = await menu.get_keyboard(user)
    msg = await call.message.answer('Меню:', reply_markup=keyboard)
    await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)

#should be down
@dp.message_handler(state="*")
async def unknown_msg(msg: types.Message):
    text = f"{msg.from_user.full_name}, ты что-то делаешь не так."
    await msg.answer(text)


@dp.callback_query_handler(state="*")
async def unknown_call(msg: types.CallbackQuery):
    text = f"{msg.from_user.full_name}, ты что-то делаешь не так."
    await msg.answer(text)
