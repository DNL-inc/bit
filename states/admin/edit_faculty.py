from aiogram.dispatcher.filters.state import State, StatesGroup


class EditFacultyStates(StatesGroup):
    create = State()
    edit = State()