from aiogram import types 
from aiogram.utils import exceptions
from loader import dp


@dp.errors_handler()
async def message_to_delete_not_found(update: types.Update, error: exceptions.MessageToDeleteNotFound):
    return True