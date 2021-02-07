from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from loader import dp, bot
from data import config

from states.menu import MenuStates
from datetime import datetime

from utils.misc import get_current_admin, get_current_user
from models import Admin, PostponeMessage, User
from states.admin import AdminStates
from states.admin.send_msg import SendMsgStates
from keyboards.inline.admin import all_postpone_msg, send_msg, delete_postpone_msg, back_after_creating
from keyboards.inline import back_callback, admin


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=AdminStates.all_states)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext, user):
    await callback.answer("Вы вернулись обратно")
    await MenuStates.admin.set()
    keyboard = await admin.get_keyboard(user)
    await callback.message.edit_text("Администрирование:", reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='send_msg'), state=AdminStates.all_states)
async def back_to_send_msg(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("Вы вернулись обратно")
    keyboard = await send_msg.get_keyboard(admin)
    await callback.message.edit_text("Выберите из предложеного в меню:", reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='delete_msg'), state=AdminStates.all_states)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    keyboard = await all_postpone_msg.get_keyboard(admin)
    await callback.message.edit_text('Все текущие сообщения: ', reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.send_msg)
async def get_menu_sender_msg(call: types.CallbackQuery, admin: Admin, state: FSMContext):
    if call.data == 'all-msgs':
        keyboard = await all_postpone_msg.get_keyboard(admin)
        await call.message.edit_text('Все текущие сообщения: ', reply_markup=keyboard)
    elif call.data.startswith('msg-'):
        message_id = call.data.split('-')[-1]
        await state.update_data(msg_id=message_id)
        await call.message.edit_text('Вы хотите удалить сообщение?', reply_markup=delete_postpone_msg.keyboard)
    elif call.data == 'delete-msg':
        data = await state.get_data()
        message_id = data.get('msg_id')
        if message_id: await PostponeMessage().delete_message(message_id)
        keyboard = await all_postpone_msg.get_keyboard(admin)
        await call.message.edit_text('Все текущие сообщения: ', reply_markup=keyboard)
    elif call.data.startswith('send-'):
        await state.update_data(destination=call.data.split('-')[-1], current_msg_id=call.message.message_id)
        await SendMsgStates.text.set()
        await call.message.edit_text('Напишите сообщение')


@get_current_admin()
@get_current_user()
@dp.message_handler(state=SendMsgStates.text)
async def get_text(msg: types.Message, admin: Admin, state: FSMContext, user: User):
    data = await state.get_data()
    message_id = data.get('current_msg_id')
    await bot.edit_message_text("Теперь нужно написать дату и время в которые вы хотите отправить пост в формате "
                                "<DD.MM.YYYY HH:MM>", user.tele_id, message_id)
    await SendMsgStates.time.set()
    await state.update_data(postpone_text=msg.text)
    await msg.delete()


@get_current_admin()
@get_current_user()
@dp.message_handler(state=SendMsgStates.time)
async def get_time(msg: types.Message, admin: Admin, state: FSMContext, user: User):
    data = await state.get_data()
    message_id = data.get('current_msg_id')
    text = data.get('postpone_text')
    sending_time: datetime
    try:
        date, time = msg.text.split()
        day, month, year = map(int, date.split('.'))
        hour, minute = map(int, time.split(':'))
        sending_time = datetime(year, month, day, hour, minute)
        if config.LOCAL_TZ.localize(sending_time) <= config.LOCAL_TZ.localize(datetime.now()):
            try:
                await bot.edit_message_text(
                    'Дата и время указывают на прошлое - сообщение не будет никогда отправленно', user.tele_id,
                    message_id)
            except MessageNotModified:
                pass
            await msg.delete()
            return
    except ValueError:
        try:
            await bot.edit_message_text('Нужно написать время в формате <DD.MM.YYYY HH:MM>', user.tele_id, message_id)
        except MessageNotModified:
            pass
        await msg.delete()
        return
    await PostponeMessage().create_message(config.LOCAL_TZ.localize(sending_time), text, admin)
    await bot.edit_message_text(
        f'Отлично, ваше сообщение будет отправленно в {sending_time.strftime("%A, %d.%m.%Y %H:%m")} с текстом "{text[:20]}..."',
        user.tele_id, message_id, reply_markup=back_after_creating.keyboard)
    await AdminStates.send_msg.set()
    await msg.delete()
