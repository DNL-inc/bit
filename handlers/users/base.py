from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from middlewares import _
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
    await callback.answer(_("Вы вернулись обратно"))
    chats = await Chat().select_chats_by_creator(user.id)
    keyboard = await get_keyboard(True)
    await callback.message.edit_text(_("Настройки:"), reply_markup=keyboard)
    await menu.MenuStates.settings.set()
