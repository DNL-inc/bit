from aiogram import types
from aiogram.dispatcher import FSMContext

from data import config
from data.config import LOCAL_TZ
from filters.is_private import IsPrivate
from keyboards.default import menu
from keyboards.inline import back_callback
from keyboards.inline.admin import edit_subgroups, cancel
from loader import dp
from models import User
from models.event import Day, Event
from states.menu import MenuStates
from utils.misc import get_current_user
from middlewares import _


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='lang'), state=MenuStates.schedule)
async def back_to_menu(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.message.delete()
    await call.answer(_("Ты вернулся обратно"))
    await MenuStates.mediate.set()
    keyboard = await menu.get_keyboard(user)
    msg = await call.message.answer(_('Меню:'), reply_markup=keyboard)
    await state.update_data(current_msg=msg.message_id, current_msg_text=msg.text)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='subgroups'), state=MenuStates.schedule)
async def back_to_menu(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer(_("Ты вернулся назад"))
    await user.fetch_related("group")
    keyboard = await edit_subgroups.get_keyboard(user.group.id, False, True, user)
    await call.message.edit_text(_('Расписание:'), reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(back_callback.filter(category='cancel'), state=MenuStates.schedule)
async def back_to_menu(call: types.CallbackQuery, user: User, state: FSMContext):
    await call.answer(_("Ты вернулся обратно"))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for day in Day:
        keyboard.add(types.InlineKeyboardButton(day.name, callback_data=day.name))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='subgroups')))

    await call.message.edit_text(_('Выбери день недели:'), reply_markup=keyboard)


@get_current_user()
@dp.callback_query_handler(IsPrivate(), state=MenuStates.schedule)
async def schedule_manager(callback: types.CallbackQuery, state: FSMContext, user: User):
    await callback.answer()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for day in Day:
        keyboard.add(types.InlineKeyboardButton(day.name, callback_data=day.name))
    keyboard.add(types.InlineKeyboardButton(_('Назад'), callback_data=back_callback.new(category='subgroups')))
    if callback.data.startswith('subgroup-'):
        await state.update_data(subgroup=int(callback.data.split('-')[-1]))
        await callback.message.edit_text(_('Выбери день недели:'), reply_markup=keyboard)
    elif callback.data == 'all-events':
        await callback.message.edit_text(_('Выбери день недели:'), reply_markup=keyboard)
    elif callback.data in [day.name for day in Day]:
        await state.update_data(day=callback.data)
        data = await state.get_data()
        events = None
        if data.get('subgroup'):
            events = await Event.filter(subgroup=data.get('subgroup'), day=callback.data).order_by('time',
                                                                                                   'time').all()
        else:
            await user.fetch_related("group")
            events = await Event.filter(group=user.group.id, day=callback.data).order_by('time',
                                                                                         'time').all()
        text = _("**Расписание**\n")
        for i in range(1, len(events) + 1):
            text += "{}. **{}** [{}]({}) в {}\n".format(i, config.TYPE_EVENT.get(events[i - 1].type),
                                                        events[i - 1].title if len(events[i - 1].title) < 12 else
                                                        events[i - 1].title[:12] + "...",
                                                        events[i - 1].link,
                                                        events[i - 1].time.strftime('%H:%M'))
        await callback.message.edit_text(text, reply_markup=cancel.keyboard, parse_mode="Markdown",
                                         disable_web_page_preview=True)
