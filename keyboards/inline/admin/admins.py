from aiogram import types
from middlewares import _
from data.config import LOCAL_TZ
from models import Admin, User, PostponeMessage
from keyboards.inline import blank_callback, back_callback


async def get_keyboard(admin: Admin):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    admins = None
    if admin.role.name == 'supreme':
        admins = await Admin.all()
    elif admin.role.name == 'improved':
        admins = await Admin.filter(role="ordinary", faculty=admin.faculty_id).all()
    if admins:
        for a in admins:
            await a.fetch_related("group")
            await a.fetch_related("faculty")
            await a.fetch_related('user')
            if a.role.name == 'ordinary':
                keyboard.add(
                    types.InlineKeyboardButton("Админ {} - ".format(a.faculty.title) + a.group.title,
                                               callback_data='admin-' + str(a.id)))
            elif a.role.name == 'improved':
                keyboard.add(types.InlineKeyboardButton("Админ факультета - " + a.faculty.title,
                                                        callback_data='admin-' + str(a.id)))
            else:
                keyboard.add(
                    types.InlineKeyboardButton("Джедай - " + a.user.username, callback_data='admin-' + str(a.id)))
    else:
        keyboard.add(
            types.InlineKeyboardButton(_("Нет тут ничего"), callback_data=blank_callback.new(category='blank')))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='lang')))
    return keyboard
