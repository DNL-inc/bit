from telebot import types
import telebot
from models.base import register_user, is_admin_bool, register_fac, session, Faculty
from admin import AdminPanel, menu_markup, group_markup
from group import GroupPanel, faculties_markup

from menu import get_main_menu, course_markup, schedule_markup

bot = telebot.TeleBot(token='992816254:AAHc_pVKMqESQ84bjp_I80-AYertBBt7F80')
admin_panel = AdminPanel(bot)
group_panel = GroupPanel(bot)


def menu(message):
    chat_id = message.from_user.id
    if is_admin_bool(message):
        bot.send_message(chat_id, "Выберіть щось",
                         reply_markup=get_main_menu(message, True))
    else:
        bot.send_message(chat_id, "Выберіть щось",
                         reply_markup=get_main_menu(message, False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    register_user(message)
    menu(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_menu(message):
    if message.text == "Рaспиcание":
        response_schedule(message)
    elif message.text == "Админиcтрировaниe":
        admin_panel.get_menu(message)
    elif message.text == "Група":
        group_panel.choose_fac(message)


def response_schedule(message):
    bot.delete_message(message_id=message.message_id,
                       chat_id=message.from_user.id)
    chat_id = message.from_user.id
    bot.send_message(chat_id, 'Виберіть день:', reply_markup=schedule_markup())


@bot.callback_query_handler(func=lambda call: True)
def handler_calls(call):
    # admin-panel
    # -----> button create group <-------
    if call.data == 'add_group_btn':
        admin_panel.choose_faculty_interface(call)
    # -------> section choosing facutly <----------
    elif call.data.startswith('admin-faculty-'):
        admin_panel.choose_course_interface(call)
    elif call.data == 'backChooseFaculty':
        bot.edit_message_text('Меню:', chat_id=call.from_user.id, message_id=call.message.message_id,
                              reply_markup=menu_markup(admin_panel.get_admin(call)))
    # -------> section choosing course <----------
    elif call.data.startswith('admin-course-'):
        admin_panel.add_group_interface(call)
    elif call.data.startswith('backChooseCourse-'):
        bot.edit_message_text("Выберите факультет:", chat_id=call.from_user.id,
                              message_id=call.message.message_id, reply_markup=faculties_markup())
    # --------> button create faculty <--------
    elif call.data == 'add_fac_btn':
        admin_panel.add_fac_interface(call)
    # group-panel
    # -------> section choosing facutly <----------
    elif call.data.startswith("faculty-"):
        group_panel.choose_course(call)
    elif call.data.startswith('backChooseCourse'):
        bot.edit_message_text("Выберите факультет:", chat_id=call.from_user.id,
                              message_id=call.message.message_id, reply_markup=faculties_markup())

    # -------> section choosing course <----------
    elif call.data.startswith('course-'):
        group_panel.choose_group(call)
    elif call.data == 'backChooseGroup':
        bot.edit_message_text("Выберите курс:", chat_id=call.from_user.id,
                              message_id=call.message.message_id, reply_markup=course_markup())

    elif call.data.startswith('group-'): group_panel.call_save_group(call)

                

if __name__ == "__main__":
    bot.polling()
