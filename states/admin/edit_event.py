from aiogram.dispatcher.filters.state import StatesGroup, State


class EditEventStates(StatesGroup):
    event = State()
    link = State()
    title = State()
    type = State()
    over = State()
    day = State()
    operation = State()
