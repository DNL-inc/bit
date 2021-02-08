from aiogram.dispatcher.filters.state import State, StatesGroup

from states.base.choose_group import ChooseGroupStates


class EditGroupStates(ChooseGroupStates):
    create = State()
    edit = State()
