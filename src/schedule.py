import re
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from telebot import types
from models.base import (Event, User, session)
from menu import course_markup, get_main_menu

Session = sessionmaker(bind = engine)
session = Session()


def schedule_classes(message, day, group):
        markup = types.InlineKeyboardMarkup(row_width=1)
        events = session.query(Event).filter(Event.day == day, Event.group == group).all()
        for event in events:
            bot.send_message(message.from_user.id, text=event.title)
        markup.add(types.InlineKeyboardButton(text='Назад', callback_data="-schedule-day"))
        return markup

def schedule_markup(caption="", back=""):
        markup = types.InlineKeyboardMarkup(row_width=1)
        monday = types.InlineKeyboardButton(text='Понеділок', callback_data="schedule-monday")
        tuesday = types.InlineKeyboardButton(text='Вівторок', callback_data="schedule-tuesday")
        wednesday = types.InlineKeyboardButton(text='Середа', callback_data="schedule-wednesday")
        thursday = types.InlineKeyboardButton(text='Четвер', callback_data="schedule-thursday")
        friday = types.InlineKeyboardButton(text='П\'ятниця', callback_data="schedule-friday")
        saturday = types.InlineKeyboardButton(text='Субота', callback_data="schedule-saturday")
        sunday = types.InlineKeyboardButton(text='Неділя', callback_data="schedule-sunday")
        markup.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        if back != "":
            markup.add(types.InlineKeyboardButton(text='Назад', callback_data=back))
        return markup

class SchedulePanel:
    def __init__(self, bot):
        self.bot = bot

    def print_classes(self, message):
        self

    def get_classes(self, message):
        self.bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
        self.bot.send_message(message.from_user.id, "Выберите день:", reply_markup=schedule_markup(caption=message, back="schedule-day"))

    def callback_handler_sched(self, call):
        if call.data == 'schedule-day':
            schedule_markup(caption=message, back="schedule-day")
    


