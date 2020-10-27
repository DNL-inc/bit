from telebot import types
import telebot
from models import register_user

bot = telebot.TeleBot(token='992816254:AAHc_pVKMqESQ84bjp_I80-AYertBBt7F80')


def menu(message):
    chat_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(row_width=1)
    schedule_item = types.KeyboardButton('/1. Расписание')
    markup.add(schedule_item)
    bot.send_message(chat_id, "Выбери что-то", reply_markup=markup)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    register_user(message)
    menu(message)


@bot.message_handler(commands=['1.'])
def response_schedule(message):
    chat_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=1)
    monday = types.InlineKeyboardButton(text='Понедельник', callback_data="schedule_monday")
    tuesday = types.InlineKeyboardButton(text='Вторник', callback_data="schedule_tuesday")
    wednesday = types.InlineKeyboardButton(text='Среда', callback_data="schedule_wednesday")
    thursday = types.InlineKeyboardButton(text='Четверг', callback_data="schedule_thursday")
    friday = types.InlineKeyboardButton(text='Пятница', callback_data="schedule_friday")
    markup.add(monday, tuesday, wednesday, thursday, friday)
    bot.send_message(chat_id, 'Выберите день:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def get_schedule(call):
    if call.data == 'schedule_monday':
        bot.answer_callback_query(call.id, text="""
        Ох, понедельние будет тяжёлым...
        """)
        bot.send_message(call.from_user.id, """
1. Арх Комп
2. Прога
        """)

if __name__ == "__main__":
    bot.polling()

