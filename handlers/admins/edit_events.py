import re
from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from keyboards.inline import events, day, back_callback, delete_callback
from keyboards.inline.admin import edit_subgroups, event_operations, cancel, event_type, cancel_or_delete
from loader import dp, bot
from models import Admin, Event, User
from states.admin import AdminStates
from states.admin.edit_event import EditEventStates
from utils.misc import get_current_admin, get_current_user


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=EditEventStates.all_states)
async def back_to_choose_subgroup(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await AdminStates.events.set()
    await admin.fetch_related('group')
    keyboard = await edit_subgroups.get_keyboard(admin.group.id, editable=False, for_events=True)
    await callback.message.edit_text('Выберите подгруппу:', reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='subgroup'), state=EditEventStates.all_states)
async def back_to_choose_day(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.message.edit_text("Выберите день: ", reply_markup=day.keyboard)
    await EditEventStates.day.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='event'), state=EditEventStates.all_states)
async def back_to_choose_event(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    data = await state.get_data()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=data.get('day'), subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.events)
async def entry_manage_events(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
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
    await state.update_data(day=callback.data)
    data = await state.get_data()
    await admin.fetch_related("group")
    keyboard = await events.get_keyboard(day=callback.data, subgroup_id=data.get('subgroup_id'), editable=True,
                                         group_id=admin.group.id)
    await callback.message.edit_text("Выберите событие или создайте новое:", reply_markup=keyboard)
    await EditEventStates.event.set()


@dp.callback_query_handler(state=EditEventStates.event)
async def choose_event(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.startswith('event-'):
        event_id = callback.data.split('-')[-1]
        event_id = int(event_id)
        await state.update_data(event_id=event_id)
        event = await Event.get(id=event_id)
        date = event.event_over.strftime("%A, %d.%m.%Y") if event.event_over else "-"
        await callback.message.edit_text('''
Название: [{}]({})
Тип: {}
Дата: {}
        '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
                                         parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                         disable_web_page_preview=True)
        await EditEventStates.operation.set()


@dp.callback_query_handler(back_callback.filter(category='cancel'), state=EditEventStates.all_states)
async def back_choose_day(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    date = event.event_over.strftime("%A, %d.%m.%Y") if event.event_over else "-"
    await callback.message.edit_text('''
Название: [{}]({})
Тип: {}
Дата: {}
    '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
                                     parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                     disable_web_page_preview=True)


@get_current_admin()
@dp.callback_query_handler(delete_callback.filter(category='event'), state=EditEventStates.operation)
async def delete_event(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
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
    elif callback.data == 'delete':
        data = await state.get_data()
        event = await Event.get(id=data.get('event_id'))
        keyboard = await cancel_or_delete.get_keyboard('event')
        await callback.message.edit_text('Уверены, что хотите удалить "{}"?'.format(event.title),
                                         reply_markup=keyboard, disable_web_page_preview=True)


@get_current_user()
@dp.message_handler(state=EditEventStates.title)
async def change_title(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    if event:
        event.title = msg.text
        await event.save()
    date = event.event_over.strftime("%A, %d.%m.%Y") if event.event_over else "-"
    await bot.edit_message_text('''
Название: [{}]({})
Тип: {}
Дата: {}
    '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
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
        date = event.event_over.strftime("%A, %d.%m.%Y") if event.event_over else "-"
        await bot.edit_message_text('''
Название: [{}]({})
Тип: {}
Дата: {}
            '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
                                    parse_mode="Markdown", reply_markup=event_operations.keyboard, chat_id=user.tele_id,
                                    message_id=data.get('current_msg'), disable_web_page_preview=True)
        await EditEventStates.operation.set()
    else:
        await bot.edit_message_text("Cсылку не правильная", reply_markup=cancel.keyboard, chat_id=user.tele_id,
                                    message_id=data.get('current_msg'))


@get_current_user()
@dp.message_handler(state=EditEventStates.over)
async def change_date(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    await msg.delete()
    day, month, year = map(int, msg.text.split('.'))
    try:
        date_over = datetime(year, month, day)
        if config.LOCAL_TZ.localize(date_over) >= config.LOCAL_TZ.localize(datetime.now()):
            if event:
                event.event_over = date_over
                await event.save()
                date = date_over.strftime("%A, %d.%m.%Y") if date_over else "-"
                await bot.edit_message_text('''
Название: [{}]({})
Тип: {}
Дата: {}
                    '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
                                            parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                            chat_id=user.tele_id,
                                            message_id=data.get('current_msg'), disable_web_page_preview=True)
            await EditEventStates.operation.set()
        else:
            await bot.edit_message_text(
                'Дата указывает на прошлое', user.tele_id,
                message_id=data.get('current_msg'))
    except ValueError:
        await bot.edit_message_text(
            'Дата указана неправильно', user.tele_id,
            message_id=data.get('current_msg'))


@get_current_user()
@dp.callback_query_handler(state=EditEventStates.type)
async def change_type(callback: types.CallbackQuery, state: FSMContext, user: User):
    data = await state.get_data()
    event = await Event.get(id=data.get('event_id'))
    if event:
        event.type = callback.data
        await event.save()
    date = event.event_over.strftime("%A, %d.%m.%Y") if event.event_over else "-"
    await callback.message.edit_text('''
Название: [{}]({})
Тип: {}
Дата: {}
    '''.format(event.title, event.link, config.TYPE_EVENT[event.type], date),
                                     parse_mode="Markdown", reply_markup=event_operations.keyboard,
                                     disable_web_page_preview=True)
    await EditEventStates.operation.set()
