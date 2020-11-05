from telebot import types
import telebot
from models.base import register_user, is_admin_bool, register_group, register_fac
from admin import AdminPanel, menu_markup

from menu import get_main_menu

bot = telebot.TeleBot(token='992816254:AAHc_pVKMqESQ84bjp_I80-AYertBBt7F80')
admin_panel = AdminPanel(bot)

def menu(message):
    chat_id = message.from_user.id
    if is_admin_bool(message):
        bot.send_message(chat_id, "Выберіть щось", reply_markup=get_main_menu(message, True))
    else:
        bot.send_message(chat_id, "Выберіть щось", reply_markup=get_main_menu(message, False))


@bot.message_handler(commands=['start', 'help'])
def start(message):
    register_user(message)
    menu(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_menu(message):
    if message.text == "Рaспиcание": response_schedule(message)
    elif message.text == "Админиcтрировaниe": admin_panel.get_menu(message)
    elif message.text == "Група": choose_course(message)

def course_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    firstCourse = types.InlineKeyboardButton(text='1-й курс', callback_data="first") 
    secondCourse = types.InlineKeyboardButton(text='2-й курс', callback_data="second") 
    thirrdCourse = types.InlineKeyboardButton(text='3-й курс', callback_data="third") 
    fourthCouse = types.InlineKeyboardButton(text='4-й курс', callback_data="fourth") 
    fifthCourse = types.InlineKeyboardButton(text='5-й курс', callback_data="fifth") 
    sixthCourse = types.InlineKeyboardButton(text='6-й курс', callback_data="sixth")
    markup.add(firstCourse, secondCourse, thirrdCourse, fourthCouse, fifthCourse, sixthCourse)
    return markup

def group_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    group1 = types.InlineKeyboardButton(text='ІПЗ-11', callback_data="ipz11")
    group2 = types.InlineKeyboardButton(text='ІПЗ-12', callback_data="ipz12")
    group3 = types.InlineKeyboardButton(text='ІПЗ-13', callback_data="ipz13")
    backButton = types.InlineKeyboardButton(text='Назад', callback_data="backChooseGroup")
    markup.add(group1, group2, group3, backButton)
    return markup

def choose_course(message):
    bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    chat_id = message.from_user.id
    bot.send_message(chat_id, 'Виберіть курс:', reply_markup=course_markup())
    

def choose_group(message):
    chat_id = message.from_user.id
    bot.edit_message_text(chat_id=chat_id, message_id=message.message.message_id, text='Виберіть группу:', reply_markup=group_markup())
    
def response_schedule(message):
    bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    chat_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    monday = types.InlineKeyboardButton(
        text='Понеділок', callback_data="schedule_monday")
    tuesday = types.InlineKeyboardButton(
        text='Вівторок', callback_data="schedule_tuesday")
    wednesday = types.InlineKeyboardButton(
        text='Середа', callback_data="schedule_wednesday")
    thursday = types.InlineKeyboardButton(
        text='Четвер', callback_data="schedule_thursday")
    friday = types.InlineKeyboardButton(
        text='П\'ятниця', callback_data="schedule_friday")
    markup.add(monday, tuesday, wednesday, thursday, friday)
    bot.send_message(chat_id, 'Виберіть день:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handler_calls(call):
    if call.data == 'schedule_monday':
        bot.answer_callback_query(call.id, text="""
        Ох, понедельние будет тяжёлым...
        """)
        bot.send_photo(call.from_user.id, 'https://imgur.com/5a7A1oh')
        bot.send_message(call.from_user.id, """
09:00 - 10:20 [Основи программування(Л)](https://us02web.zoom.us/j/84711450833)
10:30 - 11:50 [Архітектура комп'ютера(Л)](https://us02web.zoom.us/j/6547310436?pwd=YXZ3OEE1ZlpqVVhPdXFqMEJxcXBXUT09)
12:10 - 13:30 [Основи программування(П)](https://us04web.zoom.us/j/2308670388?pwd=T01hczE3ZkRjWkZiWUNLV1prNlBTUT09)
13:40 - 15:00 [Архітектура комп'ютера(П)](https://us04web.zoom.us/j/71126649979?pwd=Ry9ScFhCblk0TDREbDRGbFIySjNBUT09)
15:10 - to the enernity [Архітектура комп'ютера(К)](https://us02web.zoom.us/j/6547310436?pwd=YXZ3OEE1ZlpqVVhPdXFqMEJxcXBXUT09)
        """, parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'schedule_tuesday':
        bot.send_photo(call.from_user.id, 'https://imgur.com/g24rPtv')
        bot.send_message(call.from_user.id, """
09:00 - 10:20 [Дискретна математика(Л)](https://us02web.zoom.us/j/9590521136?pwd=TW90dVlOU01QU1JrSHIxOFNtR2p1Zz09)
10:30 - 11:50 [Дискретна математика(П)](https://us02web.zoom.us/j/9590521136?pwd=TW90dVlOU01QU1JrSHIxOFNtR2p1Zz09)
12:10 - 13:30 Chill time
13:40 - 15:00 [Іноземна мова(П)](https://us04web.zoom.us/j/7591896666?pwd=OHJhNjRRSTJxMUN3V1ZBTGdhMFVxZz09&nbsp;)
""", parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'schedule_wednesday':
        bot.send_photo(call.from_user.id, 'https://imgur.com/OPGBKpZ')
        bot.send_message(call.from_user.id, """
09:00 - 10:20 Chill time
10:30 - 11:50 [Основи математики(Л)](https://us04web.zoom.us/j/72854542678?pwd=dkswUUs1YUFmZitDVDFOcUN2amRGQT09)
12:10 - 13:30 [Вступ до університетсьских студій](https://meet.google.com/cwj-ugif-mhr?pli=1&amp;authuser=1&amp;hma=1&amp;hmv=1)
13:40 - 15:00 Chill time
""", parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'schedule_thursday':
        bot.send_photo(call.from_user.id, 'https://imgur.com/Of4UgMr')
        bot.send_message(call.from_user.id, """
09:00 - 10:20 Chill time
10:30 - 11:50 [Основи программування(Л)](https://us02web.zoom.us/j/84711450833)
12:10 - 13:30 [Основи математики(П)](https://us04web.zoom.us/j/77436934907?pwd=bEdWMjg2eDFOd0N2YXBZSVdKOGZvUT09)
13:40 - 15:00 [Основи программування(П)](https://us04web.zoom.us/j/2308670388?pwd=T01hczE3ZkRjWkZiWUNLV1prNlBTUT09)
""", parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'schedule_friday':
        bot.send_photo(call.from_user.id, 'https://imgur.com/wVKhF2m')
        bot.send_message(call.from_user.id, """
09:00 - 10:20 [Іноземна мова(П)](https://us04web.zoom.us/j/7591896666?pwd=OHJhNjRRSTJxMUN3V1ZBTGdhMFVxZz09&nbsp;)
10:30 - 11:50 [Іноземна мова(П)](https://us04web.zoom.us/j/7591896666?pwd=OHJhNjRRSTJxMUN3V1ZBTGdhMFVxZz09&nbsp;)
12:10 - 13:30 [Іноземна мова(П)](https://us04web.zoom.us/j/7591896666?pwd=OHJhNjRRSTJxMUN3V1ZBTGdhMFVxZz09&nbsp;)
13:40 - 15:00 Chill time
""", parse_mode='Markdown', disable_web_page_preview=True)


    elif call.data == 'first': choose_group(call)
    elif call.data == 'backChooseGroup': bot.edit_message_text('Виберіть группу:', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=course_markup())
    elif call.data == 'add_group_btn': admin_panel.choose_course_interface(call)

    elif call.data == 'backChooseCourse': bot.edit_message_text('Меню:', chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=menu_markup(admin_panel.get_admin(call)))
    # elif call.data.endswith('_admin'): admin_panel.add_group_interface(call)
    # elif call.data.startswith('course_'): register_group(call)
    elif call.data == 'add_fac_btn': admin_panel.add_fac_interface(call)

if __name__ == "__main__": 
    bot.polling()