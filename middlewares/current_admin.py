from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram import types
from models import Admin


class CurrentAdminMiddleware(BaseMiddleware):
    async def on_process_message(self, msg: types.Message, data: dict):
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_admin', False):
            admin = await Admin().select_admin_by_tele_id(msg.from_user.id)
            if admin:
                data['admin'] = admin
            else:
                await msg.answer("""
Похоже, что вы не админ, напишите сюда @kidden.      
                """)
                raise CancelHandler()

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        handler = current_handler.get()
        if handler and getattr(handler, 'get_current_admin', False):
            admin = await Admin().select_admin_by_tele_id(callback.from_user.id)
            if admin:
                data['admin'] = admin
            else:
                await callbackы.answer("""
Похоже, что вы не админ, напишите сюда @kidden.   
                """)
                raise CancelHandler()