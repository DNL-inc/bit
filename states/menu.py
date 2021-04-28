from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class MenuStates(StatesGroup):
    schedule = State()
    admin = State()
    settings = State()
    mediate = State()