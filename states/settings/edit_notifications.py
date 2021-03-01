from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class EditNotificationsStates(StatesGroup):
    day = State()
    event = State()
