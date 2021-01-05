from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from filters.isAdmin import IsAdminFilter

from .start import start

def setup(db: Dispatcher):
    db.register_message_handler(start, CommandStart())