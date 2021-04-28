from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingsGandSStates(StatesGroup):
    faculty = State()
    course = State()
    group = State()
    subgroups = State()