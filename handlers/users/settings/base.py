from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from keyboards.inline import languages, back_callback, soon_be_available, notification, chats
from keyboards.inline.settings import get_keyboard
from utils.misc import get_current_user
from models import User, Chat
from states import menu, settings
from data import config
from . import group_and_subgroups, notifications, chat_settings


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=settings.SettingsStates.all_states)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer("Вы вернулись обратно")
    keyboard = await get_keyboard(True)
    await callback.message.edit_text("Настройки:", reply_markup=keyboard)
    await menu.MenuStates.settings.set()


async def get_langs(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer()
    keyboard = await languages.get_keyboard()
    await call.message.edit_text('Выбери язык:', reply_markup=keyboard)
    await settings.SettingsStates.lang.set()


@get_current_user()
@dp.callback_query_handler(state=menu.MenuStates.settings)
async def get_section_settings(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer()
    if call.data == 'group-and-subgroups':
        await settings.SettingsStates.group_and_subgroups.set()
        await group_and_subgroups.get(call, user, state)
    elif call.data == 'chat-settings':
        await settings.SettingsStates.chat_settings.set()
        keyboard = await chats.get_keyboard(user.id, True)
        await call.message.edit_text('Чаты:',
                                     reply_markup=keyboard)
    elif call.data == 'notifications':
        await settings.SettingsStates.notifications.set()
        keyboard = await notification.get_keyboard(user)
        await call.message.edit_text('Уведомления:', reply_markup=keyboard)
    elif call.data == 'lang':
        await get_langs(call, user, state)


@get_current_user()
@dp.callback_query_handler(state=settings.SettingsStates.lang)
async def choose_lang(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data in config.LANGUAGES.keys():
        await User().update_user(user.tele_id, lang=call.data)
        await call.answer('Язык установлен')
        await call.message.edit_text("Вы успешно изменили группу и подгруппы!")
        await call.message.delete()
        keyboard = await get_keyboard(True)
        msg = await call.message.answer("Вы успешно изменили язык!", reply_markup=keyboard)
        await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)
        await menu.MenuStates.settings.set()

# # should be down
# @dp.message_handler(state="*")
# async def unknown_msg(msg: types.Message, state: FSMContext):
#     state = await state.get_state()
#     text = f"""
# {msg.from_user.full_name}, ты что-то делаешь не так.
# Эхо в состоянии <code>{state}</code>"""
#     await msg.answer(text)
#
#
# @dp.callback_query_handler(state="*")
# async def unknown_call(msg: types.CallbackQuery, state: FSMContext):
#     state = await state.get_state()
#     text = f"""
# {msg.from_user.full_name}, ты что-то делаешь не так.
# Эхо в состоянии <code>{state}</code>"""
#     await msg.answer(text)
