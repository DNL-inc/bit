from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthStates(StatesGroup):
    choose_lang = State()
    choose_faculty = State()
    choose_course = State()
    choose_group = State()
    choose_subgroups = State()