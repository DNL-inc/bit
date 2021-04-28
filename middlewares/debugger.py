from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types
from models import User


class Debugger(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        print('go through')

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        print('go through')
