from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.is_chat import IsChat
from loader import dp, bot
from models import User, Chat, Code
from states import menu
from states.chat import ChatStates
from states.menu import MenuStates
from utils.misc import get_current_user


@dp.message_handler(IsChat(), commands=['menu'], state='*')
async def show_menu(msg: types.Message):
    chat = await Chat.filter(tele_id=msg.chat.id).first()
    if chat:
        await msg.reply('hello')
        await ChatStates.mediate.set()
    else:
        await msg.reply('Сперва отправьте мне код!')
        await ChatStates.wait_for_code.set()


@get_current_user()
@dp.message_handler(IsChat(), state=ChatStates.wait_for_code)
async def check_code(msg: types.Message, user: User):
    code = await Code.filter(key=msg.text, user=user).first()
    print(msg)
    if code:
        await msg.reply('Вы добавили группу')
        await ChatStates.mediate.set()
        await Chat.create(tele_id=msg.chat.id, creator=user, title=msg.chat.title)
        await code.delete()
    else:
        await msg.reply('Код неправильный')
