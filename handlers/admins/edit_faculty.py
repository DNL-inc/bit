from aiogram import types
from aiogram.dispatcher import FSMContext
from tortoise.exceptions import IntegrityError

from keyboards.inline import back_callback, faculties, delete_callback, create_callback
from keyboards.inline.admin import cancel, cancel_or_delete, cancel_or_create
from loader import dp, bot
from models import Admin, Faculty, User
from states.admin import AdminStates
from states.admin.edit_faculty import EditFacultyStates
from utils.misc import get_current_admin, get_current_user


@get_current_admin()
@dp.callback_query_handler(delete_callback.filter(category='faculty'), state=EditFacultyStates.edit)
async def delete_faculty(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    data = await state.get_data()
    faculty_id = data.get('faculty')
    faculty = await Faculty.filter(id=faculty_id).first()
    await faculty.delete()
    await state.update_data(faculty=None)
    await callback.answer('Факультет был удален')
    await admin.fetch_related("faculty")
    keyboard = await faculties.get_keyboard(True if admin.role.name == 'supreme' else False,
                                            admin.faculty if admin.role.name == 'improved' else False)
    await callback.message.edit_text('Выберите факультет или добавть новый', reply_markup=keyboard)
    await AdminStates.faculties.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='cancel'),
                           state=[AdminStates.faculties, EditFacultyStates.create, EditFacultyStates.edit])
async def back_from_faculty(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    data = await state.get_state()
    await callback.answer()
    await admin.fetch_related("faculty")
    keyboard = await faculties.get_keyboard(True if admin.role.name == 'supreme' else False,
                                            admin.faculty if admin.role.name == 'improved' else False)
    await callback.message.edit_text('Выберите факультет или добавть новый', reply_markup=keyboard)
    await AdminStates.faculties.set()


@get_current_admin()
@get_current_user()
@dp.callback_query_handler(create_callback.filter(category='faculty'), state=EditFacultyStates.edit)
async def save_faculty(callback: types.CallbackQuery, state: FSMContext, user: User, admin: Admin):
    data = await state.get_data()
    faculty_id = data.get('faculty')
    faculty = await Faculty.filter(id=faculty_id).first()
    faculty.title = data.get('new_faculty').upper() if data.get('new_faculty') else None
    try:
        await faculty.save()
    except IntegrityError:
        await callback.answer('Такой факультет уже существует')
    await admin.fetch_related("faculty")
    keyboard = await faculties.get_keyboard(True if admin.role.name == 'supreme' else False,
                                            admin.faculty if admin.role.name == 'improved' else False)
    await callback.answer("Вы успешно изменили название факультета")
    await bot.edit_message_text("Выберите факультет или добавть новый", reply_markup=keyboard, chat_id=user.tele_id,
                                message_id=data.get("current_msg"))
    await AdminStates.faculties.set()


@get_current_admin()
@get_current_user()
@dp.message_handler(state=EditFacultyStates.create)
async def create_faculty(msg: types.Message, state: FSMContext, user: User, admin: Admin):
    data = await state.get_data()
    await msg.delete()
    try:
        await Faculty.create(title=msg.text.upper())
    except IntegrityError:
        await bot.edit_message_text('Такой факультет уже существует', reply_markup=cancel.keyboard,
                                    chat_id=user.tele_id,
                                    message_id=data.get("current_msg"))
        return
    await admin.fetch_related("faculty")
    keyboard = await faculties.get_keyboard(True if admin.role.name == 'supreme' else False,
                                            admin.faculty if admin.role.name == 'improved' else False)
    await bot.edit_message_text("Выберите факультет или добавть новый", reply_markup=keyboard, chat_id=user.tele_id,
                                message_id=data.get("current_msg"))
    await AdminStates.faculties.set()


@get_current_user()
@dp.message_handler(state=EditFacultyStates.edit)
async def edit_faculty(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    faculty_id = data.get('faculty')
    await msg.delete()
    if faculty_id:
        faculty = await Faculty.filter(id=faculty_id).first()
        keyboard = await cancel_or_create.get_keyboard("faculty")
        await state.update_data(new_faculty=msg.text)
        await bot.edit_message_text(
            'Вы пытаетесь изменить название факультета "{}" на "{}"'.format(faculty.title, msg.text),
            reply_markup=keyboard, chat_id=user.tele_id, message_id=data.get("current_msg"))


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.faculties)
async def edit_faculties(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await callback.answer()
    if callback.data == "add-faculty":
        await callback.message.edit_text('Напишите название нового факультета', reply_markup=cancel.keyboard)
        await EditFacultyStates.create.set()
    elif callback.data.startswith("faculty-"):
        faculty_id = callback.data.split('-')[-1]
        faculty = await Faculty.filter(id=int(faculty_id)).first()
        keyboard = await cancel_or_delete.get_keyboard("faculty")
        await callback.message.edit_text('Напишите название для факультета - {}, чтобы изменить'.format(faculty.title),
                                         reply_markup=keyboard)
        await EditFacultyStates.edit.set()
        await state.update_data(faculty=int(faculty_id))


@dp.message_handler(state=AdminStates.faculties)
async def clear(msg: types.Message):
    await msg.delete()
