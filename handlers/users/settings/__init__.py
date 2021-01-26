from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from keyboards.inline import languages, back_callback, soon_be_available
from keyboards.inline.settings import get_keyboard
from utils.misc import get_current_user
from models import User, Chat
from states import menu, settings
from data import config
from . import group_and_subgroups, notifications, chat_settings
 

async def get_langs(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer()
    keyboard = await languages.get_keyboard()
    await call.message.edit_text('Выбери язык:', reply_markup=keyboard)
    await settings.SettingsStates.lang.set()


@get_current_user()
@dp.callback_query_handler(state=menu.MenuStates.settings)
async def get_section_settings(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data == 'group-and-subgroups':
        await settings.SettingsStates.group_and_subgroups.set()
        await group_and_subgroups.get(call, user, state)
    elif call.data == 'chat-settings':
        await settings.SettingsStates.chat_settings.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим', reply_markup=soon_be_available.keyboard)
    elif call.data == 'notifications':
        await settings.SettingsStates.notifications.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим', reply_markup=soon_be_available.keyboard)
    elif call.data == 'lang':
        keyboard = await languages.get_keyboard()
        await get_langs(call, user, state)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=settings.SettingsStates.all_states)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer("Вы вернулись обратно")
    chats = await Chat().select_chats_by_creator(user.id)
    keyboard = await get_keyboard(True if chats else False)
    await callback.message.edit_text("Настройки:", reply_markup=keyboard)
    await menu.MenuStates.settings.set()


@get_current_user()
@dp.callback_query_handler(state=settings.SettingsStates.lang)
async def choose_lang(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data in config.LANGUAGES.keys():
        await User().update_user(user.tele_id, lang=call.data)
        await call.answer('Язык установлен')
        await call.message.edit_text("Вы успешно изменили группу и подгруппы!")
        await call.message.delete()
        chats = await Chat().select_chats_by_creator(user.id)
        keyboard = await get_keyboard(True if chats else False)
        msg = await call.message.answer("Вы успешно изменили язык!", reply_markup=keyboard)
        await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)
        await menu.MenuStates.settings.set()
