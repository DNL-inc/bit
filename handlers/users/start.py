from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from filters.is_private import IsPrivate
from loader import dp
from middlewares import _
from models import User
from utils.misc import rate_limit, get_current_user
from states.auth import AuthStates
from states.menu import MenuStates
from keyboards.inline import languages, back_callback, faculties
from keyboards.default import menu


@dp.message_handler(IsPrivate(), CommandStart(), state='*')
async def start(msg: types.Message, state: FSMContext):
    is_created = await User().create_user(tele_id=msg.from_user.id, firstname=msg.from_user.first_name,
                                          lastname=msg.from_user.last_name, username=msg.from_user.username,
                                          welcome_message_id=0)
    if is_created:
        welcome_message = await msg.answer(_("""
    Привет! Меня зовут bit и я попытаюсь сделать твою студентскую жизнь более приятной!

**Как пользоваться**
📌 Чтобы подписаться на расписание группы просто пройди простую регистрацию при первом запуске или выбери группу в разделе «Настройки», сразу после этого переходи в «Расписание», выбирай нужный день, чтобы увидеть расписание.

📌 Если хочешь, чтобы я напоминал тебе про начало событий из расписания перейди в «Настройки», затем «Уведомления» и следуй инструкциям.

📌 Если хочешь добавить меня в чат группы и получать ссылки на пары, переходи в соотвествующий раздел в настройках и следуй инструкциям.

**Обратная связь**
Я работаю некорректно или ты нашёл какой-то баг? - Напиши моему хозяину: 
@kidden

**Команды**
/help - увидеть инструкцию по использованию снова.
/menu - выход в главное меню.
    """))
        is_created.welcome_message_id = welcome_message.message_id
        await is_created.save()
        # На каком языке ты предпочитаешь общаться?
        keyboard = await faculties.get_keyboard()
        await msg.answer(
            _("Прежде чем приступить к использованию, давай познакомимся поближе! На каком факультете ты учишься?"),
            reply_markup=keyboard)
        await AuthStates.choose_lang.set()
        await msg.delete()
    else:
        await msg.delete()
        user = await User().select_user_by_tele_id(msg.from_user.id)
        keyboard = await menu.get_keyboard(user)
        msg = await msg.answer(_("Давно тебя не было в Уличных Гонках! Заходи!"))
        await msg.answer(_(
            "Чёрт.. Не тот скрипт.. Я имею в виду, что мы с тобой уже знакомы. Если хочешь посмотреть расписание или поковыряться в настройках - просто нажми на соответсвующие кнопки меню.\nПо всем вопросам: @kidden"),
            reply_markup=keyboard)
        await MenuStates.mediate.set()
        await state.update_data(current_msg_text=msg.text, current_msg=msg.message_id)


@rate_limit(10, 'blank')
@dp.callback_query_handler(text_contains='blank', state="*")
async def blank_calls(call: types.CallbackQuery):
    await call.answer(cache_time=60, text=_('Хватит тыкать! Я с первого раза всё понимаю..'))
