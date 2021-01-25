from aiogram import types
from aiogram.dispatcher import FSMContext
from data import config
from keyboards.inline import (back_callback, courses, faculties, groups,
                              languages, subgroups)
from loader import dp
from models import User
from states.auth import AuthStates
from states.menu import MenuStates
from utils.misc import get_current_user, rate_limit
from keyboards.default import menu   



@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=AuthStates.choose_faculty)
async def back_choose_lang(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись обратно")
    await callback.message.edit_text("Выбери язык: ", reply_markup=languages.keyboard)
    await AuthStates.choose_lang.set()


@get_current_user()
@rate_limit(2, 'lang')
@dp.callback_query_handler(state=AuthStates.choose_lang)
async def choose_lang(callback: types.CallbackQuery, state: FSMContext):
    if callback.data in config.LANGUAGES.keys():
        await state.update_data(lang=callback.data)
        keyboard = await faculties.get_keyboard()
        await callback.answer("Язык установлен")
        await callback.message.edit_text("Выберите ваш факультет:", reply_markup=keyboard)
        await AuthStates.next()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='faculty'), state=AuthStates.choose_course)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись обратно")
    keyboard = await faculties.get_keyboard()
    await callback.message.edit_text("Выберите ваш факультет:", reply_markup=keyboard)
    await AuthStates.choose_faculty.set()


@get_current_user()
@rate_limit(2, 'faculty')
@dp.callback_query_handler(state=AuthStates.choose_faculty)
async def choose_faculty(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.startswith('faculty'):
        await state.update_data(faculty=callback.data.split('-')[-1])
        await callback.answer("Факультет выбран")
        await callback.message.edit_text("Выберите ваш курс:", reply_markup=courses.keyboard)
        await AuthStates.next()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='course'), state=AuthStates.choose_group)
async def back_choose_course(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer("Вы вернулись обратно")
    await callback.message.edit_text("Выберите ваш курс:", reply_markup=courses.keyboard)
    await AuthStates.choose_course.set()


@get_current_user()
@rate_limit(2, 'course')
@dp.callback_query_handler(state=AuthStates.choose_course)
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
        await AuthStates.next()


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='group'), state=AuthStates.choose_subgroups)
async def back_choose_group(callback: types.CallbackQuery, state: FSMContext):
    args = await state.get_data()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    keyboard = await groups.get_keyboard(data)
    await callback.answer("Вы вернулись обратно")
    await callback.message.edit_text("Выберите вашу группу:", reply_markup=keyboard)
    await AuthStates.choose_group.set()


@get_current_user()
@dp.callback_query_handler(state=AuthStates.choose_group)
async def choose_group(callback: types.CallbackQuery, state: FSMContext, user: User):
    if callback.data.startswith('group'):
        await state.update_data(group_id=int(callback.data.split('-')[-1]))
        await callback.answer("Группа выбрана")
        data = await state.get_data()
        group_id = data['group_id']
        user_subgroups = await User().select_user_subgroups(user)
        keyboard = await subgroups.get_keyboard(group_id, user_subgroups)
        await callback.message.edit_text("Выберите вашу подгруппу:", reply_markup=keyboard)
        await AuthStates.next()


@get_current_user()
@dp.callback_query_handler(text='auth_complete', state=AuthStates.choose_subgroups)
async def auth_complete(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer()
    data = await state.get_data()
    await User().update_user(user.tele_id, lang=data.get('lang'), group=data.get('group_id'))
    await state.finish()
    await callback.message.edit_text("Вы успешно прошли регистрацию!")
    await MenuStates.mediate.set()
    keyboard = await menu.get_keyboard(user)
    await callback.message.delete()
    msg = await callback.message.answer("Вы успешно прошли регистрацию!", reply_markup=keyboard)
    await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)
    

@get_current_user()
@dp.callback_query_handler(state=AuthStates.choose_subgroups)
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
