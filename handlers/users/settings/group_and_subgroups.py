from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline import (back_callback, blank_callback, courses,
                              faculties, groups, settings, subgroups)
from loader import dp
from models import User, Chat
from states.menu import MenuStates
from states.settings import SettingsStates, group_and_subgroups
from utils.misc import get_current_user

@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=group_and_subgroups.SettingsGandSStates.faculty)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext, user):
    await callback.answer("Вы вернулись обратно")
    await MenuStates.settings.set()
    chats = await Chat().select_chats_by_creator(user.id)
    keyboard = await settings.get_keyboard(True if chats else False)
    await callback.message.edit_text("Настроки:", reply_markup=keyboard)
    

async def get(callback: types.CallbackQuery, user: User, state: FSMContext):
    keyboard = await faculties.get_keyboard()
    await callback.message.edit_text("Выберите ваш факультет:", reply_markup=keyboard)
    await group_and_subgroups.SettingsGandSStates.faculty.set()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='faculty'), state=group_and_subgroups.SettingsGandSStates.course)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись обратно")
    keyboard = await faculties.get_keyboard()
    await callback.message.edit_text("Выберите ваш факультет:", reply_markup=keyboard)
    await group_and_subgroups.SettingsGandSStates.faculty.set()


@get_current_user()
@dp.callback_query_handler(state=group_and_subgroups.SettingsGandSStates.faculty)
async def choose_faculty(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.startswith('faculty'):
        await state.update_data(faculty=callback.data.split('-')[-1])
        await callback.answer("Факультет выбран")
        await callback.message.edit_text("Выберите ваш курс:", reply_markup=courses.keyboard)
        await group_and_subgroups.SettingsGandSStates.next()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='course'), state=group_and_subgroups.SettingsGandSStates.group)
async def back_choose_course(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись обратно")
    await callback.message.edit_text("Выберите ваш курс:", reply_markup=courses.keyboard)
    await group_and_subgroups.SettingsGandSStates.course.set()


@get_current_user()
@dp.callback_query_handler(state=group_and_subgroups.SettingsGandSStates.course)
async def choose_course(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.startswith('course'):
        await state.update_data(course=callback.data.split('-')[-1])
        await callback.answer("Курс выбран")
        args = await state.get_data()
        data = dict()
        data['faculty'] = args['faculty']
        data['course'] = args['course']
        keyboard = await groups.get_keyboard(data)
        await callback.message.edit_text("Выберите вашу группу:", reply_markup=keyboard)
        await group_and_subgroups.SettingsGandSStates.next()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='group'), state=group_and_subgroups.SettingsGandSStates.subgroups)
async def back_choose_group(callback: types.CallbackQuery, state: FSMContext):
    args = await state.get_data()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    keyboard = await groups.get_keyboard(data)
    await callback.answer("Вы вернулись обратно")
    await callback.message.edit_text("Выберите вашу группу:", reply_markup=keyboard)
    await group_and_subgroups.SettingsGandSStates.group.set()


@get_current_user()
@dp.callback_query_handler(state=group_and_subgroups.SettingsGandSStates.group)
async def choose_group(callback: types.CallbackQuery, state: FSMContext, user: User):
    if callback.data.startswith('group'):
        await state.update_data(group_id=int(callback.data.split('-')[-1]))
        await callback.answer("Группа выбрана")
        data = await state.get_data()
        group_id = data['group_id']
        user_subgroups = await User().select_user_subgroups(user)
        keyboard = await subgroups.get_keyboard(group_id, user_subgroups)
        await callback.message.edit_text("Выберите вашу подгруппу:", reply_markup=keyboard)
        await group_and_subgroups.SettingsGandSStates.next()


@get_current_user()
@dp.callback_query_handler(text='complete', state=group_and_subgroups.SettingsGandSStates.subgroups)
async def complete(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer()
    data = await state.get_data()
    await User().update_user(user.tele_id, lang=data.get('lang'), group=data.get('group_id'))
    await state.finish()
    await MenuStates.mediate.set()
    await callback.message.edit_text("Вы успешно изменили группу и подгруппы!")
    chats = await Chat().select_chats_by_creator(user.id)
    keyboard = await settings.get_keyboard(True if chats else False)
    await callback.message.delete()
    msg = await callback.message.answer("Вы успешно изменили группу и подгруппы!", reply_markup=keyboard)
    await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)


@get_current_user()
@dp.callback_query_handler(state=group_and_subgroups.SettingsGandSStates.subgroups)
async def choose_subgroups(callback: types.CallbackQuery, state: FSMContext, user: User):
    if callback.data.startswith('subgroup'):
        subgroup = int(callback.data.split('-')[-1])
        data = await state.get_data()
        group_id = data['group_id']
        await User().add_or_clear_subgroup(subgroup, user)
        await callback.answer()
        user_subgroups = await User().select_user_subgroups(user)
        keyboard = await subgroups.get_keyboard(group_id, user_subgroups)
        await callback.message.edit_text("Выберите ваши подгруппы:", reply_markup=keyboard)
