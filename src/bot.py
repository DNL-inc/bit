from telebot import types
import telebot
from models.base import register_user, is_admin_bool, register_fac, session, Faculty
from admin import AdminPanel
from group import GroupPanel, faculties_markup
from schedule import SchedulePanel, schedule_markup

from menu import get_main_menu, course_markup, schedule_markup
from config import config
import logging
import ssl

from aiohttp import web
from os import getcwd

BASE_DIR = getcwd()

WEBHOOK_SSL_CERT = BASE_DIR+'/webhook_cert.pem'
WEBHOOK_SSL_PRIV = BASE_DIR+'/webhook_pkey.pem'

telebot.logger.setLevel(logging.INFO)

app = web.Application()

bot = telebot.TeleBot(token=config.token, parse_mode='markdown')
admin_panel = AdminPanel(bot)
group_panel = GroupPanel(bot)
schedule_panel = SchedulePanel(bot)

async def handle(request):
    if request.match_info.get('token') == bot.token:
        request_body_dict = await request.json()
        update = telebot.types.Update.de_json(request_body_dict)
        bot.process_new_updates([update])
        return web.Response()
    else:
        return web.Response(status=403)

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)
app.add_routes([web.post('/{token}/', handle),])

def menu(message):
    chat_id = message.from_user.id
    if is_admin_bool(message):
        bot.send_message(chat_id, text='Выберите что-то:', reply_markup=get_main_menu(message, True))
    else:
        bot.send_message(chat_id, text='Выберите что-то:',reply_markup=get_main_menu(message, False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    register_user(message)
    bot.send_message(message.from_user.id, """
*Как пользоваться*

Чтобы подписаться на расписание группы нажми _«Группа»_, выбери свой факультет, курс и группу, затем переходи в _«Расписание»_ и выбери нужный день, чтобы увидеть расписание. 

*Обратная связь*

Есть идеи по улучшению бота или нашёл какой-то баг? - Напиши нам: 
@kidden

/start - увидеть это сообщение снова.
/menu — вернуться в главное меню.""", parse_mode='Markdown')
    menu(message)

@bot.message_handler(commands=['menu'])
def show_main_menu(message):
    menu(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_menu(message):
    if message.text == "Рaспиcание":
        schedule_panel.get_days(message)
    elif message.text == "Админиcтрировaниe":
        admin_panel.get_menu(message)
    elif message.text == "Грyппa":
        group_panel.choose_fac(message)


def response_schedule(message):
    bot.delete_message(message_id=message.message_id,
                       chat_id=message.from_user.id)
    chat_id = message.from_user.id
    bot.send_message(chat_id, 'Виберите день:', reply_markup=schedule_markup())


@bot.callback_query_handler(func=lambda call: True)
def handler_calls(call):
    # admin-panel
    if call.data.startswith('admin'):
        admin_panel.callback_handler(call)
    # group-panel
    elif call.data.startswith("group"):
        group_panel.callback_handler(call)
    # schedule-panel
    elif call.data.startswith('schedule'):
        schedule_panel.callback_handler(call)
                
bot.remove_webhook()
bot.set_webhook(url=config.webhook_url_base + config.webhook_url_path, certificate=open(WEBHOOK_SSL_CERT, 'r'))
web.run_app(app, host=config.webhook_listen, port=config.port, ssl_context=context)
