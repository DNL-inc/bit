import re
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from telebot import types
from models.base import (Event, User, session, engine)
from menu import course_markup, get_main_menu, schedule_markup
import os

BASE_DIR = os.getcwd()

Session = sessionmaker(bind = engine)
session = Session()


class SchedulePanel:
    def __init__(self, bot):
        self.bot = bot

    def get_days(self, message):
        try: message.message_id
        except AttributeError: pass
        else: self.bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
        self.bot.send_message(message.from_user.id, "Выберите день:", reply_markup=schedule_markup(caption="schedule"))
    
    def get_list_lessons(self, message):
        day = message.data.split('_')[-1]
        tele_id = message.from_user.id
        group = session.query(User).filter(User.tele_id == tele_id).first().group
        photo = open(BASE_DIR+'/src/img/'+day+'.jpg', mode='rb')
        self.bot.send_photo(message.from_user.id, photo=photo)
        events = session.query(Event).filter(Event.day == day, Event.group == group)
        events = events.order_by(-Event.time_start.desc()).all()
        for event in events[:-1]:
            self.bot.send_message(message.from_user.id, text=event.time_start.strftime('%H:%M')+" "+event.title, disable_web_page_preview=True)
        if events:
            self.bot.send_message(message.from_user.id, text=events[-1].time_start.strftime('%H:%M')+" "+events[-1].title, disable_web_page_preview=True)
        else:
            self.bot.send_message(message.from_user.id, text="Сегодня тусим")

    def callback_handler(self, call):
        if call.data.startswith('schedule-'):
            self.get_list_lessons(call)

