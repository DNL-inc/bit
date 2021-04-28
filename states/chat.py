from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatStates(StatesGroup):
    wait_for_code = State()
    schedule = State()
    mediate = State()
