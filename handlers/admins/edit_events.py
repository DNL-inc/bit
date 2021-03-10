import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified

from data import config
from data.config import LOCAL_TZ
from keyboards.inline import events, day, back_callback, delete_callback, create_callback, continue_callback
from keyboards.inline.admin import edit_subgroups, event_operations, cancel, event_type, cancel_or_delete, \
    cancel_or_create, continue_or_cancel
from loader import dp, bot
from models import Admin, Event, User
from states.admin import AdminStates
from states.admin.create_event import CreateEventStates
from states.admin.edit_event import EditEventStates
from utils.misc import get_current_admin, get_current_user


def get_event_template(event):
    date = event.event_over.strftime("%d.%m.%Y") if event.event_over else "-"
    return """
Название: [{}]({})
Тип: {}
Дата: {}
Время: {}
    """.format(event.title, event.link, config.TYPE_EVENT.get(event.type), date, event.time.strftime("%H:%M"))


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='lang'),
                           state=EditEventStates.all_states)
async def back_to_choose_subgroup(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("")
    await AdminStates.events.set()
    await admin.fetch_related('group')
    keyboard = await edit_subgroups.get_keyboard(admin.group.id, editable=False, for_events=True)
    await callback.message.edit_text('Выберите подгруппу:', reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='subgroup'),
                           state=EditEventStates.all_states)
async def back_to_choose_day(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("")
    await callback.message.edit_text("Выберите день: ", reply_markup=day.keyboard)
    await EditEventStates.day.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='event'),
                           state=EditEventStates.all_states)
async def back_to_choose_event(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("")
    data = await state.get_data()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=data.get('day'), subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.events)
async def entry_manage_events(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("")
    if callback.data == "all-events":
        await callback.message.edit_text("Выберите день: ", reply_markup=day.keyboard)
    elif callback.data.startswith('subgroup-'):
        subgroup_id = callback.data.split('-')[-1]
        subgroup_id = int(subgroup_id)
        await callback.message.edit_text("Выберите день: ", reply_markup=day.keyboard)
        await state.update_data(subgroup_id=subgroup_id)

    await EditEventStates.day.set()


@get_current_admin()
@dp.callback_query_handler(state=EditEventStates.day)
async def choose_day(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("День выбран")
    await state.update_data(day=callback.data)
    data = await state.get_data()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=callback.data, subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@dp.callback_query_handler(state=EditEventStates.event)
async def choose_event(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Событие выбрано")
    if callback.data.startswith('event-'):
        event_id = callback.data.split('-')[-1]
        event_id = int(event_id)
        await state.update_data(event_id=event_id)
        event = await Event.get(id=event_id)

        await callback.message.edit_text(get_event_template(event),
                                         parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                         disable_web_page_preview=True)
        await EditEventStates.operation.set()

    elif callback.data == 'add-event':
        await callback.message.edit_text("Выберите тип:", reply_markup=event_type.keyboard)
        await CreateEventStates.type.set()


@dp.callback_query_handler(back_callback.filter(category='cancel'),
                           state=EditEventStates.all_states)
async def back_choose_day(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись назад")
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))

    await callback.message.edit_text(get_event_template(event),
                                     parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                     disable_web_page_preview=True)
    await EditEventStates.operation.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='cancel'),
                           state=CreateEventStates.all_states)
async def back_choose_event(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("Вы вернулись назад")
    data = await state.get_data()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=data.get('day'), subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@get_current_admin()
@dp.callback_query_handler(delete_callback.filter(category='event'), state=EditEventStates.operation)
async def delete_event(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer("Событие удалено")
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    if event:
        await event.delete()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=data.get('day'), subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)


@dp.callback_query_handler(state=EditEventStates.operation)
async def choose_operation(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Выбрано событие")
    if callback.data == 'edit-title':
        await callback.message.edit_text("Напишите новое название события", reply_markup=cancel.keyboard)
        await EditEventStates.title.set()
    elif callback.data == 'edit-type':
        await callback.message.edit_text("Выберите тип:", reply_markup=event_type.keyboard)
        await EditEventStates.type.set()
    elif callback.data == 'edit-date':
        await callback.message.edit_text("Напишите новую дату события", reply_markup=cancel.keyboard)
        await EditEventStates.over.set()
    elif callback.data == 'edit-link':
        await callback.message.edit_text("Напишите новую ссылку", reply_markup=cancel.keyboard)
        await EditEventStates.link.set()
    elif callback.data == 'edit-time':
        await callback.message.edit_text("Напишите время начало пары", reply_markup=cancel.keyboard)
        await EditEventStates.time.set()
    elif callback.data == 'delete':
        data = await state.get_data()
        event = await Event.get(id=data.get('event_id'))
        keyboard = await cancel_or_delete.get_keyboard('event')
        await callback.message.edit_text('Уверены, что хотите удалить "{}"?'.format(event.title),
                                         reply_markup=keyboard, disable_web_page_preview=True)


@get_current_admin()
@get_current_user()
@dp.message_handler(state=EditEventStates.time)
async def change_time(msg: types.Message, state: FSMContext, user: User, admin: Admin):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    try:
        hour, minute = map(int, msg.text.split(':'))
        if event:
            event.time = datetime(year=1991, month=8, day=24, hour=hour, minute=minute)
            await event.save()
        await admin.fetch_related("group")
        await bot.edit_message_text(get_event_template(event),
                                    parse_mode="Markdown", reply_markup=event_operations.keyboard, chat_id=user.tele_id,
                                    message_id=data.get('current_msg'), disable_web_page_preview=True)
        await EditEventStates.operation.set()

    except ValueError:
        await bot.edit_message_text("Неправильный формат или не правильно указано время", user.tele_id,
                                    data.get('current_msg'), reply_markup=cancel.keyboard)


@get_current_user()
@dp.message_handler(state=EditEventStates.title)
async def change_title(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    if event:
        event.title = msg.text
        await event.save()

    await bot.edit_message_text(get_event_template(event),
                                parse_mode="Markdown", reply_markup=event_operations.keyboard, chat_id=user.tele_id,
                                message_id=data.get('current_msg'), disable_web_page_preview=True)
    await EditEventStates.operation.set()


@get_current_user()
@dp.message_handler(state=EditEventStates.link)
async def change_link(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    if re.match(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
            msg.text):
        if event:
            event.link = msg.text
            await event.save()

        await bot.edit_message_text(get_event_template(event),
                                    parse_mode="Markdown", reply_markup=event_operations.keyboard, chat_id=user.tele_id,
                                    message_id=data.get('current_msg'), disable_web_page_preview=True)
        await EditEventStates.operation.set()
    else:
        try:

            await bot.edit_message_text("Cсылку неправильная", reply_markup=cancel.keyboard, chat_id=user.tele_id,
                                        message_id=data.get('current_msg'))
        except MessageNotModified:
            pass


@get_current_user()
@dp.message_handler(state=EditEventStates.over)
async def change_date(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    day, month, year = map(int, msg.text.split('.'))
    try:
        date_over = datetime(year, month, day)
        timestamp_now = LOCAL_TZ.localize(datetime.now())
        timestamp = LOCAL_TZ.localize(
            datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day))
        if config.LOCAL_TZ.localize(date_over) >= timestamp:
            if event:
                event.event_over = date_over
                await event.save()
                date = date_over.strftime("%A, %d.%m.%Y") if date_over else "-"
                await bot.edit_message_text(get_event_template(event),
                                            parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                            chat_id=user.tele_id,
                                            message_id=data.get('current_msg'), disable_web_page_preview=True)
            await EditEventStates.operation.set()
        else:
            try:
                await bot.edit_message_text(
                    'Дата указывает на прошлое', user.tele_id,
                    message_id=data.get('current_msg'))
            except MessageNotModified:
                pass
    except ValueError:
        try:
            await bot.edit_message_text(
                'Дата указана неправильно', user.tele_id,
                message_id=data.get('current_msg'))
        except MessageNotModified:
            pass


@get_current_user()
@dp.callback_query_handler(state=EditEventStates.type)
async def change_type(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer("Выбрано событие")
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    if event:
        event.type = callback.data
        await event.save()

    await callback.message.edit_text(get_event_template(event),
                                     parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                     disable_web_page_preview=True)
    await EditEventStates.operation.set()


@dp.callback_query_handler(state=CreateEventStates.type)
async def get_type(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Тип выбран")
    await state.update_data(type_event=callback.data)
    await callback.message.edit_text("Напишите название события", reply_markup=cancel.keyboard)
    await CreateEventStates.title.set()


@get_current_user()
@dp.message_handler(state=CreateEventStates.title)
async def get_title(msg: types.Message, state: FSMContext, user: User):
    await msg.delete()
    await state.update_data(title=msg.text)
    data = await state.get_data()
    keyboard = await continue_or_cancel.get_keyboard('event')
    await bot.edit_message_text("Напишите дату до которой будет существовать событие", reply_markup=keyboard,
                                chat_id=user.tele_id,
                                message_id=data.get('current_msg'))
    await CreateEventStates.over.set()


@get_current_user()
@dp.callback_query_handler(continue_callback.filter(), state=CreateEventStates.over)
async def go_to_link(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer("")
    data = await state.get_data()
    await bot.edit_message_text("Напишите ссылку на событие", reply_markup=cancel.keyboard,
                                chat_id=user.tele_id,
                                message_id=data.get('current_msg'))
    await CreateEventStates.link.set()


@get_current_user()
@dp.message_handler(state=CreateEventStates.over)
async def get_event_over(msg: types.Message, state: FSMContext, user: User):
    await msg.delete()
    data = await state.get_data()
    day, month, year = map(int, msg.text.split('.'))
    try:
        date_over = datetime(year, month, day)
        timestamp_now = LOCAL_TZ.localize(datetime.now())
        timestamp = LOCAL_TZ.localize(
            datetime(timestamp_now.year, timestamp_now.month, timestamp_now.day))
        if config.LOCAL_TZ.localize(date_over) >= timestamp:
            await state.update_data(event_over=date_over)
            await CreateEventStates.link.set()
            await bot.edit_message_text("Напишите ссылку на событие", reply_markup=cancel.keyboard,
                                        chat_id=user.tele_id,
                                        message_id=data.get('current_msg'))
        else:
            try:
                await bot.edit_message_text(
                    'Дата указывает на прошлое', user.tele_id,
                    message_id=data.get('current_msg'), reply_markup=cancel.keyboard)
            except MessageNotModified:
                pass
    except ValueError:
        try:
            await bot.edit_message_text(
                'Дата указана неправильно', user.tele_id,
                message_id=data.get('current_msg'), reply_markup=cancel.keyboard)
        except MessageNotModified:
            pass


@get_current_user()
@get_current_admin()
@dp.callback_query_handler(create_callback.filter(category='event'), state=CreateEventStates.event)
async def create_event(callback: types.CallbackQuery, state: FSMContext, user: User, admin: Admin):
    await callback.answer("Событие создано")
    data = await state.get_data()
    await admin.fetch_related("group")
    await Event.create(title=data.get('title'), day=data.get('day'), type=data.get('type_event'),
                       link=data.get('link'), event_over=data.get('event_over'), group_id=admin.group.id,
                       subgroup_id=data.get('subgroup_id'), time=data.get('time'))
    keyboard = await events.get_keyboard(day=data.get('day'), subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@get_current_admin()
@get_current_user()
@dp.message_handler(state=CreateEventStates.time)
async def set_time(msg: types.Message, state: FSMContext, user: User, admin: Admin):
    data = await state.get_data()
    await msg.delete()
    try:
        hour, minute = map(int, msg.text.split(':'))
        time = datetime(year=1991, month=8, day=24, hour=hour, minute=minute)
        await state.update_data(time=time)
        await admin.fetch_related("group")
        keyboard = await cancel_or_create.get_keyboard('event')
        date = data.get('event_over').strftime("%A, %d.%m.%Y") if data.get('event_over') else "-"
        await bot.edit_message_text(
            '''
Название: [{}]({})
Тип: {}
Дата: {}
Время: {}
            '''.format(data.get('title'), data.get('link'), config.TYPE_EVENT[data.get('type_event')], date,
                       time.strftime("%H:%M")),
            user.tele_id,
            message_id=data.get('current_msg'), reply_markup=keyboard, parse_mode="Markdown")
        await CreateEventStates.event.set()

    except ValueError:
        await bot.edit_message_text("Неправильный формат или не правильно указано время", user.tele_id,
                                    data.get('current_msg'), reply_markup=cancel.keyboard)


@get_current_user()
@dp.message_handler(state=CreateEventStates.link)
async def get_link(msg: types.Message, state: FSMContext, user: User):
    await msg.delete()
    data = await state.get_data()
    if re.match(
            '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
            msg.text):
        await state.update_data(link=msg.text)
        await bot.edit_message_text("Напишите время начала события",
                                    user.tele_id,
                                    message_id=data.get('current_msg'), reply_markup=cancel.keyboard,
                                    parse_mode="Markdown")
        await CreateEventStates.time.set()
    else:
        try:
            await bot.edit_message_text(
                'Ссылка неправильная', user.tele_id,
                message_id=data.get('current_msg'), reply_markup=cancel.keyboard)
        except MessageNotModified:
            pass


@dp.message_handler(state=AdminStates.events)
async def clear(msg: types.Message):
    await msg.delete()
