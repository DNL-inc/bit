from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp

from utils.misc import get_current_user
from models import User
from states import menu, settings
from data import config
from . import group_and_subgroups, lang, notifications, chat_settings

@get_current_user()
@dp.callback_query_handler(state=menu.MenuStates.settings)
async def get_section_settings(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data == 'group-and-subgroups':
        await settings.SettingsStates.group_and_subgroups.set()
        await group_and_subgroups.get(call, user, state)
    elif call.data == 'chat-settings':
        await settings.SettingsStates.chat_settings.set()
    elif call.data == 'notifications':
        await settings.SettingsStates.notifications.set()
    elif call.data == 'lang':
        await settings.SettingsStates.lang.set()
    

