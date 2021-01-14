from aiogram import types
from aiogram.dispatcher import FSMContext 

from loader import dp, bot
from utils.misc import rate_limit, get_current_user
from models.user import User
from keyboards.default import menu

from states.menu import MenuStates


@get_current_user()
@dp.message_handler(commands=['menu'], state=MenuStates.all_states)
async def show_menu(msg: types.Message, user: User, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    current_msg = data['current_msg']
    current_msg_text = data['current_msg_text']
    keyboard = await menu.get_keyboard(user)
    await bot.delete_message(user.tele_id, current_msg)
    await msg.answer(current_msg_text, reply_markup=keyboard)
