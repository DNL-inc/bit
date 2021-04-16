from aiogram import types
from middlewares import _
from keyboards.inline import back_callback
from models import User


async def get_keyboard(user, chat=False) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if user.notification:
        keyboard.add(types.InlineKeyboardButton(_("🔴 Выключить 🔴"), callback_data='notification-trigger'))
        keyboard.add(types.InlineKeyboardButton(_('⏳ Время оповещения ⏳'), callback_data='time-notification'))
        if not chat:
            keyboard.add(types.InlineKeyboardButton(_('🗓 Cписок напоминаний 🗓'), callback_data='notifications'))
    else:
        keyboard.add(types.InlineKeyboardButton(_("🟢 Включить 🟢"), callback_data='notification-trigger'))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='settings')))
    return keyboard
