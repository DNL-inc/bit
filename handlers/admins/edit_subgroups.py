from aiogram import types
from aiogram.dispatcher import FSMContext
from tortoise.exceptions import IntegrityError

from keyboards import inline
from keyboards.inline import back_callback, faculties, delete_callback, create_callback
from keyboards.inline.admin import cancel, cancel_or_delete, cancel_or_create
from loader import dp, bot
from models import Admin, subgroup, User, Subgroup
from states.admin import AdminStates
from states.admin.edit_subgroup import EditSubgroupStates
from utils.misc import get_current_admin, get_current_user


@get_current_admin()
@dp.callback_query_handler(delete_callback.filter(category='subgroup'), state=EditSubgroupStates.edit)
async def delete_subgroup(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    data = await state.get_data()
    subgroup_id = data.get('subgroup')
    subgroup = await Subgroup.filter(id=subgroup_id).first()
    await subgroup.delete()
    await state.update_data(subgroup=None)
    await callback.answer('Подгруппа была удалена')
    await admin.fetch_related('group')
    keyboard = await inline.admin.edit_subgroups.get_keyboard(admin.group.id)
    await callback.message.edit_text('Выберите подгруппу или добавть новый', reply_markup=keyboard)
    await AdminStates.subgroups.set()


@get_current_admin()
@dp.callback_query_handler(back_callback.filter(category='cancel'), state=[AdminStates.subgroups, EditSubgroupStates.create, EditSubgroupStates.edit])
async def back_from_subgroup(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await callback.answer()
    await admin.fetch_related("group")
    keyboard = await inline.admin.edit_subgroups.get_keyboard(admin.group.id)
    await callback.message.edit_text('Выберите подгруппу или добавть новый', reply_markup=keyboard)
    await AdminStates.subgroups.set()

@get_current_admin()
@get_current_user()
@dp.callback_query_handler(create_callback.filter(category='subgroup'), state=EditSubgroupStates.edit)
async def save_subgroup(callback: types.CallbackQuery, state: FSMContext, user: User, admin: Admin):

    data = await state.get_data()
    subgroup_id = data.get('subgroup')
    subgroup = await Subgroup.filter(id=subgroup_id).first()
    subgroup.title = data.get('new_subgroup') if data.get('new_subgroup') else None
    await subgroup.save()
    await admin.fetch_related('group')
    keyboard = await inline.admin.edit_subgroups.get_keyboard(admin.group.id)
    await callback.answer("Вы успешно изменили название подгруппы")
    await bot.edit_message_text("Выберите подгруппу или добавть новый", reply_markup=keyboard, chat_id=user.tele_id,
                                message_id=data.get("current_msg"))
    await AdminStates.subgroups.set()



@get_current_user()
@get_current_admin()
@dp.message_handler(state=EditSubgroupStates.create)
async def create_subgroup(msg: types.Message, state: FSMContext, user: User, admin: Admin):
    data = await state.get_data()
    await msg.delete()
    await admin.fetch_related('group')
    await Subgroup.create(title=msg.text, group=admin.group)
    keyboard = await inline.admin.edit_subgroups.get_keyboard(admin.group.id)
    await bot.edit_message_text("Выберите подгруппу или добавть новый", reply_markup=keyboard, chat_id=user.tele_id,
                                message_id=data.get("current_msg"))
    await AdminStates.subgroups.set()


@get_current_user()
@dp.message_handler(state=EditSubgroupStates.edit)
async def edit_subgroup(msg: types.Message, state: FSMContext, user: User):
    data = await state.get_data()
    subgroup_id = data.get('subgroup')
    await msg.delete()
    if subgroup_id:
        subgroup = await Subgroup.filter(id=subgroup_id).first()
        keyboard = await cancel_or_create.get_keyboard("subgroup")
        await state.update_data(new_subgroup=msg.text)
        await bot.edit_message_text(
            'Вы пытаетесь изменить название подгруппу "{}" на "{}"'.format(subgroup.title, msg.text),
            reply_markup=keyboard, chat_id=user.tele_id, message_id=data.get("current_msg"))


@get_current_admin()
@dp.callback_query_handler(state=AdminStates.subgroups)
async def edit_subgroups(callback: types.CallbackQuery, admin: Admin, state: FSMContext):
    await callback.answer()
    if callback.data == "add-subgroup":
        await callback.message.edit_text('Напишите название новой подгруппы', reply_markup=cancel.keyboard)
        await EditSubgroupStates.create.set()
    elif callback.data.startswith("subgroup-"):
        subgroup_id = callback.data.split('-')[-1]
        subgroup = await Subgroup.filter(id=int(subgroup_id)).first()
        keyboard = await cancel_or_delete.get_keyboard("subgroup")
        await callback.message.edit_text('Напишите название для подгруппы - {}, чтобы изменить'.format(subgroup.title),
                                         reply_markup=keyboard)
        await EditSubgroupStates.edit.set()
        await state.update_data(subgroup=int(subgroup_id))


@dp.message_handler(state=AdminStates.subgroups)
async def clear(msg: types.Message):
    await msg.delete()