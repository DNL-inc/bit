from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from handlers.users.settings import group_and_subgroups
from keyboards import inline
from keyboards.inline import back_callback, chats, continue_callback, notification, languages, faculties, courses, \
    groups
from keyboards.inline.admin import cancel, continue_or_cancel
from keyboards.inline.settings import get_keyboard
from loader import dp, bot
from models import User, Chat, Code
from states import settings, menu
from states.settings import SettingsStates
from states.settings.chat_settings import ChatSettingsStates
from utils.misc import get_current_user
import uuid
from middlewares import _


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=settings.SettingsStates.all_states)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer(_("Ты вернулся назад"))
    keyboard = await get_keyboard(True)
    await callback.message.edit_text(_("Настройки:"), reply_markup=keyboard)
    await menu.MenuStates.settings.set()
    await state.update_data(chat_id=None)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=ChatSettingsStates.lang)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext, user: User):
    data = await state.get_data()
    chat = await Chat.filter(id=int(data.get('chat_id'))).first()
    await callback.answer()
    keyboard = await inline.settings.get_keyboard(False)
    await callback.message.edit_text(_("Настройки чата - {}".format(chat.title)),
                                     reply_markup=keyboard)
    await ChatSettingsStates.chat.set()
    await state.update_data(chat_id=chat.id)


@get_current_user()
@dp.callback_query_handler(state=SettingsStates.chat_settings)
async def choose_course(callback: types.CallbackQuery, user: User, state: FSMContext):
    if callback.data == 'add-chat':
        await callback.answer()
        code = str(uuid.uuid4())
        await state.update_data(code=code)
        await Code.create(key=code, user=user)
        keyboard = await continue_or_cancel.get_keyboard('chat')
        await callback.message.edit_text(_("Чтобы я мог работать в чате сначала добавь меня в нужный чат, а зачем отправь этот текст '/enter {}' без скобок в чат. Сразу после этого твой чат появится в списке и ты сможешь настроить уведомления, язык и т.д.".format(code)),
                                         reply_markup=keyboard)
        await ChatSettingsStates.add_chat.set()
    if callback.data.startswith('chat-'):
        chat = await Chat.filter(id=int(callback.data.split('-')[-1])).first()
        await callback.answer()
        keyboard = await inline.settings.get_keyboard(False)
        await callback.message.edit_text(_("Настройки чата - {}".format(chat.title)),
                                         reply_markup=keyboard)
        await ChatSettingsStates.chat.set()
        await state.update_data(chat_id=chat.id)


@get_current_user()
@dp.callback_query_handler(continue_callback.filter(category='chat'), state=ChatSettingsStates.add_chat)
async def back_to_chats(callback: types.CallbackQuery, user: User, state: FSMContext):
    await callback.answer()
    await settings.SettingsStates.chat_settings.set()
    keyboard = await chats.get_keyboard(user.id, True)
    await callback.message.edit_text(_('Чаты:'),
                                     reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='cancel'), state=ChatSettingsStates.add_chat)
async def back_to_chats(callback: types.CallbackQuery, user: User, state: FSMContext):
    data = await state.get_data()
    code = await Code.filter(key=data.get('code')).first()
    await code.delete()
    await callback.answer(_("Ты вернулся назад"))
    await settings.SettingsStates.chat_settings.set()
    keyboard = await chats.get_keyboard(user.id, True)
    await callback.message.edit_text(_('Чаты:'),
                                     reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='menu'), state=ChatSettingsStates.chat)
async def back_to_chats(callback: types.CallbackQuery, user: User, state: FSMContext):
    await callback.answer(_("Ты вернулся назад"))
    await settings.SettingsStates.chat_settings.set()
    keyboard = await chats.get_keyboard(user.id, True)
    await callback.message.edit_text(_('Чаты:'),
                                     reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(state=ChatSettingsStates.chat)
async def go_to_section_settings(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer()
    if call.data == 'group-and-subgroups':
        await settings.SettingsStates.group_and_subgroups.set()
        await group_and_subgroups.get(call, user, state)
    elif call.data == 'notifications':
        data = await state.get_data()
        chat = await Chat.filter(id=int(data.get('chat_id'))).first()
        await settings.SettingsStates.notifications.set()
        keyboard = await notification.get_keyboard(chat, True)
        await call.message.edit_text(_('Уведомления:'), reply_markup=keyboard)
    elif call.data == 'lang':
        keyboard = await languages.get_keyboard()
        await call.message.edit_text(_('Выбери язык:'), reply_markup=keyboard)
        await ChatSettingsStates.lang.set()
    elif call.data == 'delete-chat':
        data = await state.get_data()
        chat = await Chat.filter(id=int(data.get('chat_id'))).first()
        await chat.delete()
        await call.answer(_("Ты вернулся назад"))
        await settings.SettingsStates.chat_settings.set()
        keyboard = await chats.get_keyboard(user.id, True)
        await call.message.edit_text(_('Чаты:'),
                                     reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(state=ChatSettingsStates.lang)
async def choose_lang(call: types.CallbackQuery, user: User, state: FSMContext):
    if call.data in config.LANGUAGES.keys():
        data = await state.get_data()
        chat = await Chat.filter(id=int(data.get('chat_id'))).first()
        chat.lang = call.data
        await chat.save()
        await call.answer(_('Язык установлен'))
        keyboard = await inline.settings.get_keyboard(False)
        await call.message.edit_text(_("Настройки чата - {}".format(chat.title)),
                                     reply_markup=keyboard)
        await ChatSettingsStates.chat.set()
        await state.update_data(chat_id=chat.id)
