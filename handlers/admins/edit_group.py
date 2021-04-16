from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import courses, groups, back_callback, faculties, delete_callback, create_callback
from keyboards.inline.admin import cancel_or_delete, cancel, cancel_or_create
from loader import dp, bot
from models import Group, Admin, User, Faculty
from states.admin import AdminStates
from states.admin.edit_group import EditGroupStates
from utils.misc import get_current_admin, get_current_user
from middlewares import _

@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='course'), state=EditGroupStates.course)
async def back_choose_course(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(_("Ты вернулся назад"))
    await EditGroupStates.faculty.set()
    await callback.message.edit_text(_('Выбери курс:'), reply_markup=courses.keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='faculty'), state=EditGroupStates.faculty)
async def back_choose_faculty(callback: types.CallbackQuery, state: FSMContext, admin: Admin):
    await callback.answer(_("Ты вернулся обратно"))
    keyboard = None
    if admin.role.name == 'supreme':
        keyboard = await faculties.get_keyboard()
    else:
        await admin.fetch_related('faculty')
        keyboard = await faculties.get_keyboard(one_faculty=admin.faculty)
    await callback.message.edit_text(_("Выбери факультет:"), reply_markup=keyboard)
    await AdminStates.groups.set()


@get_current_admin()
@dp.callback_query_handler(state=EditGroupStates.faculty)
async def choose_course(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(_("Курс выбран"))
    if callback.data.startswith('course-'):
        await EditGroupStates.course.set()
        await state.update_data(course=int(callback.data.split('-')[-1]))
        args = await state.get_data()
        data = dict()
        data['faculty'] = args['faculty']
        data['course'] = args['course']
        keyboard = await groups.get_keyboard(data, True)
        await callback.message.edit_text(_('Выбери группу:'), reply_markup=keyboard)


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.groups)
async def choose_faculty(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(_("Факультет выбран"))
    if callback.data.startswith('faculty-'):
        await EditGroupStates.faculty.set()
        await state.update_data(faculty=int(callback.data.split('-')[-1]))
        await callback.message.edit_text(_('Выбери курс:'), reply_markup=courses.keyboard)


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='cancel'), state=[EditGroupStates.edit, EditGroupStates.create])
async def back_choose_group(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    args = await state.get_data()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    keyboard = await groups.get_keyboard(data, True)
    await callback.message.edit_text(_('Выбери группу:'), reply_markup=keyboard)
    await EditGroupStates.course.set()


@get_current_admin()
@dp.callback_query_handler(state=EditGroupStates.course)
async def edit_groups(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data == "add-group":
        await callback.message.edit_text(_('Введи название для новой группы:'), reply_markup=cancel.keyboard)
        await EditGroupStates.create.set()
    elif callback.data.startswith("group-"):
        group_id = callback.data.split('-')[-1]
        group = await Group.filter(id=int(group_id)).first()
        keyboard = await cancel_or_delete.get_keyboard("group")
        await callback.message.edit_text(_('Укажи название для группы - {}, чтобы изменить:'.format(group.title)),
                                         reply_markup=keyboard)
        await EditGroupStates.edit.set()
        await state.update_data(group=int(group_id))


@get_current_user()
@dp.callback_query_handler(create_callback.filter(category='group'), state=EditGroupStates.edit)
async def save_group(callback: types.CallbackQuery, state: FSMContext, user: User):
    args = await state.get_data()
    group_id = args.get('group')
    group = await Group.filter(id=group_id).first()
    group.title = args.get('new_group').upper() if args.get('new_group') else None
    await group.save()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    keyboard = await groups.get_keyboard(data, True)
    await callback.answer(_("Группа успешно переименована"))
    await bot.edit_message_text(_("Выбери группу:"), reply_markup=keyboard, chat_id=user.tele_id, message_id=args.get("current_msg"))
    await EditGroupStates.course.set()

@get_current_admin()
@dp.callback_query_handler(delete_callback.filter(category='group'), state=EditGroupStates.edit)
async def delete_group(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    data = await state.get_data()
    group_id = data.get('group')
    group = await Group.filter(id=group_id).first()
    await group.delete()
    await state.update_data(group=None)
    await callback.answer(_('Группа была успешно удалена'))
    args = await state.get_data()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    keyboard = await groups.get_keyboard(data, True)
    await callback.message.edit_text(_('Выбери группу:'), reply_markup=keyboard)
    await EditGroupStates.course.set()


@get_current_user()
@dp.message_handler(state=EditGroupStates.edit)
async def edit_group(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    group_id = data.get('group')
    await msg.delete()
    if group_id:
        group = await Group.filter(id=group_id).first()
        keyboard = await cancel_or_create.get_keyboard("group")
        await state.update_data(new_group=msg.text)
        await bot.edit_message_text(
            _('Ты пытаешься изменить название группы "{}" на "{}"'.format(group.title, msg.text)),
            reply_markup=keyboard, chat_id=user.tele_id, message_id=data.get("current_msg"))


@dp.message_handler(state=AdminStates.groups)
async def clear(msg: types.Message):
    await msg.delete()


@get_current_user()
@dp.message_handler(state=EditGroupStates.create)
async def create_faculty(msg: types.Message, state: FSMContext, user: User):
    await msg.delete()
    args = await state.get_data()
    data = dict()
    data['faculty'] = args['faculty']
    data['course'] = args['course']
    faculty = await Faculty.filter(id=args['faculty']).first()
    await Group.create(title=msg.text.upper(), faculty=faculty, course=args['course'])
    keyboard = await groups.get_keyboard(data, True)
    await bot.edit_message_text(_("Выбери группу или добавь новую:"), reply_markup=keyboard, chat_id=user.tele_id,
                                message_id=args.get("current_msg"))
    await EditGroupStates.course.set()




