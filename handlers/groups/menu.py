from aiogram import types
from aiogram.dispatcher import FSMContext
from middlewares import _
from data import config
from filters.is_chat import IsChat
from keyboards.default import menu
from keyboards.inline import back_callback
from keyboards.inline.admin import cancel
from keyboards.inline.day import days
from loader import bot, dp
from models import User, Chat
from models.event import Day, Event
from states.menu import MenuStates
from utils.misc import get_current_user


@get_current_user()
@dp.message_handler(IsChat(), commands=['schedule'], state='*')
async def show_menu(msg: types.Message, user: User, state: FSMContext):
    chat = await Chat.filter(tele_id=msg.chat.id).first()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for day in Day:
        keyboard.add(types.InlineKeyboardButton(days.get(day.name), callback_data=day.name))
    if chat:
        await msg.reply(_('Выбери день недели:'),
                    reply_markup=keyboard)
    else:
        await msg.reply(_('Для того, чтобы я мог работать отправь мне код! Его можно найти в настройках чатов.'))
        await ChatStates.wait_for_code.set()


@get_current_user()
@dp.callback_query_handler(IsChat(), back_callback.filter(category='cancel'), state='*')
async def back_menu_sections(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for day in Day:
        keyboard.add(types.InlineKeyboardButton(days.get(day.name), callback_data=day.name))
    await callback.message.edit_text(_('Выбери день недели:'),
                                     reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(IsChat(), state='*')
async def choose_day(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data in [days.get(day.name) for day in Day]:
        await state.update_data(day=callback.data)
        chat = await Chat.filter(tele_id=callback.message.chat.id).first()
        await chat.fetch_related("group")
        events = await Event.filter(group=chat.group.id, day=callback.data).order_by('time',
                                                                                     'time').all()
        text = "**Расписание**\n"
        for i in range(1, len(events) + 1):
            text += "{}. **{}** [{}]({}) в {}\n".format(i, config.TYPE_EVENT.get(events[i - 1].type),
                                                        events[i - 1].title if len(events[i - 1].title) < 12 else
                                                        events[i - 1].title[:12] + "...",
                                                        events[i - 1].link,
                                                        events[i - 1].time.strftime('%H:%M'))
        await callback.message.edit_text(text, reply_markup=cancel.keyboard, parse_mode="Markdown",
                                         disable_web_page_preview=True)
