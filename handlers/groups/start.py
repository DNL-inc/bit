from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.is_chat import IsChat
from loader import dp, bot
from models import User, Chat, Code
from states import menu
from states.chat import ChatStates
from states.menu import MenuStates
from utils.misc import get_current_user
from middlewares import _


@dp.message_handler(IsChat(), commands=['start'], state='*')
async def show_menu(msg: types.Message):
    chat = await Chat.filter(tele_id=msg.chat.id).first()
    if chat:
        await msg.reply(_("""
**Доступные команды для бота**
/start - увидеть это сообщение снова.
/schedule - посмотреть расписание.
/enter + код - подключение бота к чату.

**Доступный фукнционал**
- Отправка ссылок на события до их начала(настраивает человек, который добавил бота в чат в настройках бота).
- Получения расписания по команде /schedule
        """), parse_mode='Markdown')
        await ChatStates.mediate.set()
    else:
        await msg.reply(_('Для того, чтобы я мог работать отправь мне код! Его можно найти в настройках чатов.'))
        await ChatStates.wait_for_code.set()


@get_current_user()
@dp.message_handler(IsChat(), commands=['enter'], state='*')
async def check_code(msg: types.Message, user: User):
    text_code = msg.text[int(msg.entities[0].length) + 1:]
    code = await Code.filter(key=text_code, user=user).first()
    if code:
        if not await Chat.filter(tele_id=msg.chat.id).first():
            await Chat.create(tele_id=msg.chat.id, creator=user, title=msg.chat.title, group_id=user.group_id)
            await msg.reply(_('Группа добавлена! Нажми /start, чтобы узнать, что я умею.'))
        else:
            await msg.reply(_("Хм.. Кто-то уже забрал себе этот чат!"))
        await code.delete()
    else:
        await msg.reply(_('Неверный код!'))
