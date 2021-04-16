from aiogram import types
from aiogram.dispatcher import FSMContext

from filters.is_private import IsPrivate
from keyboards.inline.admin import edit_subgroups
from loader import dp, bot
from middlewares import _
from models.event import Day
from utils.misc import rate_limit, get_current_user
from models import User, Admin, Chat
from keyboards.default import menu
from keyboards.inline import settings, back_callback, admin
from data import config
from states.menu import MenuStates


@get_current_user()
@dp.message_handler(IsPrivate(), commands=['menu'], state='*')
async def show_menu(msg: types.Message, user: User, state: FSMContext):
    await msg.delete()
    await MenuStates.mediate.set()
    data = await state.get_data()
    current_msg = data.get('current_msg')
    current_msg_text = data.get('current_msg_text')
    keyboard = await menu.get_keyboard(user)
    if current_msg_text and current_msg_text:
        await bot.delete_message(user.tele_id, current_msg)
        msg = await msg.answer(current_msg_text, reply_markup=keyboard)
    else:
        msg = await msg.answer(_("Меню:"), reply_markup=keyboard)
    await state.update_data(current_msg_text=msg.text, current_msg=msg.message_id)


@get_current_user()
@dp.message_handler(IsPrivate(), lambda msg: msg.text in list(config.MENU.values()), state=MenuStates.mediate)
async def set_menu_section(msg: types.Message, user: User, state: FSMContext):
    admin = await Admin().select_admin_by_user_id(user.id)
    if msg.text == config.MENU['admin'] and admin:
        await MenuStates.admin.set()
        await get_admin_page(msg, user, state)
    elif msg.text == config.MENU['schedule']:
        await MenuStates.schedule.set()
        await get_schedule_page(msg, user, state)
    elif msg.text == config.MENU['settings']:
        await get_settings_page(msg, user, state)


async def get_schedule_page(msg: types.Message, user: User, state: FSMContext):
    data = await state.get_data()
    await user.fetch_related("group")
    if user.group:
        keyboard = await edit_subgroups.get_keyboard(user.group.id, False, True, user)
        await bot.delete_message(user.tele_id, data.get('current_msg'))
        msg = await msg.answer(_('Подгруппы:'), reply_markup=keyboard)
    else:
        data = await state.get_data()
        await bot.delete_message(user.tele_id, data.get('current_msg'))
        msg = await msg.answer(_('Похоже, ты еще не выбрал свою группу.. Бегом в настройки, выбирай группу и возвращайся.'))
    await state.update_data(current_msg_text=msg.text, current_msg=msg.message_id)
    await MenuStates.schedule.set()


async def get_settings_page(msg: types.Message, user: User, state: FSMContext):
    await MenuStates.settings.set()
    await msg.delete()
    keyboard = await settings.get_keyboard(True)
    data = await state.get_data()
    await bot.delete_message(user.tele_id, data.get('current_msg'))
    msg = await msg.answer(_('Настройки:'), reply_markup=keyboard)
    await state.update_data(current_msg_text=msg.text, current_msg=msg.message_id)


async def get_admin_page(msg: types.Message, user: User, state: FSMContext):
    await msg.delete()
    keyboard = await admin.get_keyboard(user)
    data = await state.get_data()
    await bot.delete_message(user.tele_id, data.get('current_msg'))
    msg = await msg.answer(_('Администрирование:'), reply_markup=keyboard)
    await state.update_data(current_msg_text=msg.text, current_msg=msg.message_id)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='menu'), state=MenuStates.all_states)
async def back_to_menu(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.message.delete()
    await call.answer()
    await MenuStates.mediate.set()
    keyboard = await menu.get_keyboard(user)
    msg = await call.message.answer(_('Меню:'), reply_markup=keyboard)
    await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)
