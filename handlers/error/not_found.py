from aiogram import types 
from aiogram.utils import exceptions

async def message_to_delete_not_found(update: types.Update, error: exceptions.MessageToDeleteNotFound):
    return True