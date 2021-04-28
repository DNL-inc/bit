from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatSettingsStates(StatesGroup):
    add_chat = State()
    chat = State()
    notification_time = State()
    lang = State()
    group = State()
    notifications = State()
    faculty = State()
    course = State()
   