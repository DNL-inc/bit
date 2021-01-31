from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from middlewares import _

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
    await call.message.edit_text(_('Выбери язык:'), reply_markup=keyboard)
    await settings.SettingsStates.lang.set()


@get_current_user()
@dp.callback_query_handler(state=menu.MenuStates.settings)
async def get_section_settings(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data == 'group-and-subgroups':
        await settings.SettingsStates.group_and_subgroups.set()
        await group_and_subgroups.get(call, user, state)
    elif call.data == 'chat-settings':
        await settings.SettingsStates.chat_settings.set()
        await call.message.edit_text(_('Это фича пока недоступна, как только она появится мы вам сообщим'), reply_markup=soon_be_available.keyboard)
    elif call.data == 'notifications':
        await settings.SettingsStates.notifications.set()
        await call.message.edit_text(_('Это фича пока недоступна, как только она появится мы вам сообщим'), reply_markup=soon_be_available.keyboard)
    elif call.data == 'lang':
        keyboard = await languages.get_keyboard()
        await get_langs(call, user, state)




@get_current_user()
@dp.callback_query_handler(state=settings.SettingsStates.lang)
async def choose_lang(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data in config.LANGUAGES.keys():
        await User().update_user(user.tele_id, lang=call.data)
        await call.answer(_('Язык установлен', locale = call.data))
        await call.message.edit_text(_("Вы успешно изменили группу и подгруппы!", locale = call.data))
        try:
            await bot.edit_message_text(_("Привет!", locale = call.data), chat_id=user.tele_id, message_id=user.welcome_message_id)
        except MessageNotModified:
            pass
        await call.message.delete()
        chats = await Chat().select_chats_by_creator(user.id)
        keyboard = await get_keyboard(True if chats else False)
        msg = await call.message.answer(_("Вы успешно изменили язык!", locale = call.data), reply_markup=keyboard)
        await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)
        await menu.MenuStates.settings.set()
