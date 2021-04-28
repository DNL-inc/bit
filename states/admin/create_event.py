from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateEventStates(StatesGroup):
    link = State()
    title = State()
    type = State()
    over = State()
    event = State()
    time = State()
