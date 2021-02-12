from aiogram.dispatcher.filters.state import State, StatesGroup

class EditSubgroupStates(StatesGroup):
    create = State()
    edit = State()