from loader import dp

from aiogram import types
from states import menu

from states.admin import AdminStates
from utils.misc import get_current_admin
from models import Admin
from keyboards.inline import soon_be_available, faculties
from keyboards.inline.admin import send_msg



@get_current_admin()
@dp.callback_query_handler(state=menu.MenuStates.admin)
async def get_section_settings(call: types.CallbackQuery, admin: Admin):
    if call.data == 'msg-sender':
        await AdminStates.send_msg.set()
        keyboard = await send_msg.get_keyboard(admin)
        await call.message.edit_text('Выберите из предложеного в меню: ', reply_markup=keyboard)
    elif call.data == 'edit-faculties':
        await AdminStates.faculties.set()
        keyboard = await faculties.get_keyboard(True)
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
        await AdminStates.subgroups.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим', reply_markup=soon_be_available.keyboard)
    elif call.data == 'edit-events':
        await AdminStates.events.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим', reply_markup=soon_be_available.keyboard)
    elif call.data == 'edit-admins':
        await AdminStates.admins.set()
        await call.message.edit_text('Это фича пока недоступна, как только она появится мы вам сообщим', reply_markup=soon_be_available.keyboard)

