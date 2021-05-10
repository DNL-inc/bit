from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminEditStates(StatesGroup):
    base = State()
    group = State()
    faculty = State()
    course = State()
    role = State()
    delete = State()
