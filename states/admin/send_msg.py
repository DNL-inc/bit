from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMsgStates(StatesGroup):
    text = State()
    time = State()
