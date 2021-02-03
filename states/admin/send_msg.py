from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from states.base import choose_group


class SendMsgStates(choose_group.ChooseGroupStates):
    text = State()
    time = State()