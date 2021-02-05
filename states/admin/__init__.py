from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

class AdminStates(StatesGroup):
    faculties = State()
    send_msg = State()
    groups = State()
    subgroups = State()
    events = State()
    admins = State()