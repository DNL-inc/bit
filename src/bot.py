from telebot import types
import telebot
from models.base import register_user, is_admin_bool

bot = telebot.TeleBot(token='992816254:AAHc_pVKMqESQ84bjp_I80-AYertBBt7F80')


def menu(message):
    chat_id = message.from_user.id
    schedule_item = types.KeyboardButton('Рaспиcание')
    if is_admin(message):
    if is_admin_bool(message):
        admin_item = types.KeyboardButton('Админиcтрировaниe')
    else:


@bot.message_handler(commands=['start', 'help'])
def start(message):
    register_user(message)
    menu(message)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def response_menu(message):
    if message.text == "Рaспиcание": response_schedule(message)
    elif message.text == "Админиcтрировaниe": pass

    markup = types.InlineKeyboardMarkup(row_width=1)
def response_schedule(message):
    bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    chat_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    monday = types.InlineKeyboardButton(
    tuesday = types.InlineKeyboardButton(
    wednesday = types.InlineKeyboardButton(
    thursday = types.InlineKeyboardButton(
    friday = types.InlineKeyboardButton(
    markup.add(monday, tuesday, wednesday, thursday, friday)


@bot.callback_query_handler(func=lambda call: True)
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


if __name__ == "__main__":
    bot.polling()
