from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.misc import rate_limit, get_current_user
from keyboards.inline import blank_callback, back_callback
from keyboards.inline.settings import get_keyboard
from states.menu import MenuStates
from states import settings
from keyboards.default import menu
from models import User, Chat


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=settings.SettingsStates.all_states)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer("Вы вернулись обратно")
    chats = await Chat().select_chats_by_creator(user.id)
    keyboard = await get_keyboard(True if chats else False)
    await callback.message.edit_text("Настройки:", reply_markup=keyboard)
    await menu.MenuStates.settings.set()


# #should be down
# @dp.message_handler(state="*")
# async def unknown_msg(msg: types.Message, state: FSMContext):
#     state = await state.get_state()
#     text = f"""
# {msg.from_user.full_name}, ты что-то делаешь не так.
# Эхо в состоянии <code>{state}</code>"""
#     await msg.answer(text)


# @dp.callback_query_handler(state="*")
# async def unknown_call(msg: types.CallbackQuery, state: FSMContext):
#     state = await state.get_state()
#     text = f"""
# {msg.from_user.full_name}, ты что-то делаешь не так.
# Эхо в состоянии <code>{state}</code>"""
#     await msg.answer(text)

