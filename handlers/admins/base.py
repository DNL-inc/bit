from aiogram import types

from keyboards.inline import soon_be_available, faculties, back_callback
from keyboards.inline.admin import send_msg, edit_subgroups
from loader import dp
from models import Admin
from states import menu
from states.admin import AdminStates
from utils.misc import get_current_admin


@get_current_admin()
@dp.callback_query_handler(state=menu.MenuStates.admin)
async def get_section_settings(call: types.CallbackQuery, admin: Admin):
    if call.data == 'msg-sender':
        await AdminStates.send_msg.set()
        keyboard = await send_msg.get_keyboard(admin)
        await call.message.edit_text('Выберите из предложеного в меню: ', reply_markup=keyboard)
    elif call.data == 'edit-faculties':
        await AdminStates.faculties.set()
        await admin.fetch_related("faculty")
        keyboard = await faculties.get_keyboard(True if admin.role.name == 'supreme' else False,
                                                admin.faculty if admin.role.name == 'improved' else False)
        await call.message.edit_text('Выберите факультет или добавть новый', reply_markup=keyboard)
    elif call.data == 'edit-groups':
        await AdminStates.groups.set()
        keyboard = None
        if admin.role.name == 'supreme':
            keyboard = await faculties.get_keyboard()
        else:
            await admin.fetch_related('faculty')
            keyboard = await faculties.get_keyboard(one_faculty=admin.faculty)
        await call.message.edit_text('Выберите факультет', reply_markup=keyboard)
    elif call.data == 'edit-subgroups':
        await admin.fetch_related('group')
        await AdminStates.subgroups.set()
        if admin.group:
            keyboard = await edit_subgroups.get_keyboard(admin.group.id)
            await call.message.edit_text('Выберите подгруппу или добавьте новую', reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton('Назад', callback_data=back_callback.new(category='lang')))
            await call.message.edit_text('Вав! Похоже у вы не староста, как сюда попали?', reply_markup=keyboard)
    elif call.data == 'edit-events':
        await AdminStates.events.set()
        await admin.fetch_related('group')
        keyboard = await edit_subgroups.get_keyboard(admin.group.id, editable=False, for_events=True)
        await call.message.edit_text('Выберите подгруппу:', reply_markup=keyboard)
    elif call.data == 'edit-admins':
        await AdminStates.admins.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим',
                                     reply_markup=soon_be_available.keyboard)
