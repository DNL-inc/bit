from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import back_callback, faculties, groups, courses
from keyboards.inline.admin import admins, edit_admin, edit_admins, role_admin, cancel_or_create, cancel_or_delete
from keyboards.inline import groups
from loader import dp, bot
from models import Admin, User
from states.admin import AdminStates
from states.admin.edit_admins import AdminEditStates
from utils.misc import get_current_admin, get_current_user
from middlewares import _


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category="lang"), state=AdminEditStates.all_states)
async def back_admin_menu(callback: types.CallbackQuery, admin: Admin):
    await callback.answer()
    await AdminStates.admins.set()
    await callback.message.edit_text(_('Напиши username падавана, которому ты хочешь дать Силу джедая'),
                                     reply_markup=edit_admins.keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category="course"), state=AdminEditStates.all_states)
async def back_admin_menu(callback: types.CallbackQuery, admin: Admin):
    await callback.answer()
    await AdminStates.admins.set()
    await callback.message.edit_text(_('Напиши username падавана, которому ты хочешь дать Силу джедая'),
                                     reply_markup=edit_admins.keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category="faculty"), state=AdminEditStates.all_states)
async def back_admin_menu(callback: types.CallbackQuery, admin: Admin):
    await callback.answer()
    await AdminStates.admins.set()
    await callback.message.edit_text(_('Напиши username падавана, которому ты хочешь дать Силу джедая'),
                                     reply_markup=edit_admins.keyboard)


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.admins)
async def show_admins(callback: types.CallbackQuery, admin: Admin):
    await callback.answer("Список джедаев")
    keyboard = await admins.get_keyboard(admin)
    await callback.message.edit_text("У кого мы заберем Силу?", reply_markup=keyboard)
    await AdminEditStates.base.set()


@get_current_admin()
@dp.message_handler(state=AdminStates.admins)
async def get_new_admin(msg: types.Message, admin: Admin, state: FSMContext):
    text = ""
    await msg.delete()
    user = await User.filter(username=msg.text).first()
    keyboard = None

    if user:
        if await Admin.filter(user_id=user.id).exists():
            text = "Кто-то приручил твоего падавана :("
            keyboard = edit_admins.keyboard
        else:
            text = "Кто он по жизни?"
            keyboard = await role_admin.get_keyboard(admin)
            await AdminEditStates.role.set()
    else:
        text = "Такого чела даже в наших базах нет"
        keyboard = edit_admins.keyboard

    await state.update_data(user_id=user.id)
    data = await state.get_data()
    await bot.edit_message_text(text, msg.chat.id, data.get("current_msg"), reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(state=AdminEditStates.role)
async def choose_role(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await state.update_data(role=callback.data)
    await callback.answer()
    keyboard = await faculties.get_keyboard()
    if callback.data == "ordinary" and admin.role.name == "improved":
        await callback.answer()
        await state.update_data(faculty=admin.faculty_id)
        await callback.message.edit_text("Выбери курс", reply_markup=courses.keyboard)
        await AdminEditStates.course.set()
    else:
        await callback.message.edit_text("Выбери факультет", reply_markup=keyboard)
        await AdminEditStates.faculty.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminEditStates.faculty)
async def choose_faculty(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await state.update_data(faculty=callback.data.split('-')[-1])
    data = await state.get_data()
    if data.get('role') == "ordinary":
        await callback.answer()
        await callback.message.edit_text("Выбери курс", reply_markup=courses.keyboard)
        await AdminEditStates.course.set()
    else:
        await callback.answer("Список джедаев")
        if not data.get('edit'):
            await Admin.create(user_id=data.get('user_id'), faculty_id=callback.data.split('-')[-1],
                               role=data.get('role'))
        else:
            editing_admin = await Admin.filter(user_id=data.get('user_id')).first()
            editing_admin.faculty_id = callback.data.split('-')[-1]
            await editing_admin.save()
        keyboard = await admins.get_keyboard(admin)
        await callback.message.edit_text("Список джедаев", reply_markup=keyboard)
        await AdminEditStates.base.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminEditStates.course)
async def choose_course(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await state.update_data(course=callback.data.split('-')[-1])
    await callback.answer()
    args = await state.get_data()
    data = dict()
    editing_admin = None
    if args.get('edit'): editing_admin = await Admin.filter(user_id=args.get('user_id')).first()
    data['faculty'] = args.get('faculty') if not args.get('edit') else editing_admin.faculty_id
    if args.get('faculty'): data['faculty'] = args.get('faculty')
    data['course'] = args.get('course')
    keyboard = await groups.get_keyboard(data)
    await callback.message.edit_text("Выбери группу", reply_markup=keyboard)
    await AdminEditStates.group.set()


@get_current_admin()
@get_current_user()
@dp.callback_query_handler(state=AdminEditStates.group)
async def choose_group(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    data = await state.get_data()
    if not data.get('edit'):
        await Admin.create(user_id=data.get('user_id'), faculty_id=data.get('faculty'),
                           group_id=callback.data.split('-')[-1],
                           role=data.get('role'))
        await callback.answer("Список джедаев")
        keyboard = await admins.get_keyboard(admin)
        await callback.message.edit_text("Список джедаев", reply_markup=keyboard)
        await AdminEditStates.base.set()
    else:
        editing_admin = await Admin.filter(user_id=data.get('user_id')).first()
        editing_admin.group_id = callback.data.split('-')[-1]
        editing_admin.faculty_id = data.get('faculty') if data.get('faculty') else editing_admin.faculty_id
        editing_admin.role = data.get('role') if data.get('role') else editing_admin.role.name
        await editing_admin.save()
        keyboard = await admins.get_keyboard(admin)
        await callback.message.edit_text("Давай заберем Силу", reply_markup=keyboard)
        await AdminEditStates.base.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category="admins"), state=AdminEditStates.base)
async def back_show_admins(callback: types.CallbackQuery, admin: Admin):
    await callback.answer("Список джедаев")
    keyboard = await admins.get_keyboard(admin)
    await callback.message.edit_text("Давай заберем Силу", reply_markup=keyboard)
    await AdminEditStates.base.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminEditStates.base)
async def menu_edit_admin(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    if callback.data.split('-')[0] == "edit":
        await state.update_data(edit=True)
        if callback.data == "edit-group":
            await AdminEditStates.course.set()
            await callback.message.edit_text("Выбери курс", reply_markup=courses.keyboard)
        elif callback.data == "edit-faculty":
            await AdminEditStates.faculty.set()
            keyboard = await faculties.get_keyboard()
            await callback.message.edit_text("Выбери факультет", reply_markup=keyboard)
            await AdminEditStates.faculty.set()
            await state.update_data(role="ordinary")
        elif callback.data == 'edit-role':
            await AdminEditStates.role.set()
            keyboard = await role_admin.get_keyboard(admin)
            await callback.message.edit_text("Кто он по жизни?", reply_markup=keyboard)
    elif callback.data == "delete-admin":
        keyboard = await cancel_or_delete.get_keyboard("delete-admin")
        await callback.message.edit_text("Уверен?", reply_markup=keyboard)
        await AdminEditStates.delete.set()
    else:
        editing_admin = await Admin.filter(id=callback.data.split('-')[-1]).first()
        await editing_admin.fetch_related("user")
        await editing_admin.fetch_related("group")
        await editing_admin.fetch_related("faculty")
        await state.update_data(user_id=editing_admin.user.id)
        keyboard = await edit_admin.get_keyboard(editing_admin, admin)
        await callback.message.edit_text("""
Role: {}
Username: {}
Faculty: {}
Group: {}
        """.format(editing_admin.role.name, editing_admin.user.username,
                   editing_admin.faculty.title if editing_admin.faculty else "-",
                   editing_admin.group.title if editing_admin.group else "-"), reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category="cancel"))
async def back_menu_admins(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    keyboard = await admins.get_keyboard(admin)
    await callback.message.edit_text("Список джедаев", reply_markup=keyboard)
    await AdminEditStates.base.set()


@get_current_admin()
@dp.callback_query_handler(state=AdminEditStates.delete)
async def delete_admin(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    data = await state.get_data()
    delete_admin = await Admin.filter(user_id=data.get('user_id')).first()
    await delete_admin.delete()
    keyboard = await admins.get_keyboard(admin)
    await callback.message.edit_text("Список джедаев", reply_markup=keyboard)
    await AdminEditStates.base.set()
