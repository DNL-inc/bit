from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsStates(StatesGroup):
    group_and_subgroups = State()
    lang = State()
    notifications = State()
    chat_settings = State()