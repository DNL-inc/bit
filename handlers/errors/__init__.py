from aiogram import Dispatcher
from aiogram.utils import exceptions

from .not_found import message_to_delete_not_found

def setup(db: Dispatcher):
    db.register_errors_handler(message_to_delete_not_found, exceptions.MessageToDeleteNotFound)