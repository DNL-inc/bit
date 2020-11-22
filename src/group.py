
from telebot import types
from models.base import session, Faculty, Group, save_group_user, User
from menu import course_markup


def faculties_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    faculites = session.query(Faculty).all()
    for faculty in faculites:
        markup.add(types.InlineKeyboardButton(text=faculty.title,
                                              callback_data="group-faculty-"+str(faculty.id)))
    return markup


def group_markup(faculty_id, course, message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    user = session.query(User).filter(
        User.tele_id == message.from_user.id).first()
    groups = session.query(Group).filter(
        Group.faculty == faculty_id, Group.course == course).all()
    for group in groups:
        if user.group == group.id:
            markup.add(types.InlineKeyboardButton(
                text=group.title+'✅', callback_data="group-id-"+str(group.id)))
        else:
            markup.add(types.InlineKeyboardButton(
                text=group.title, callback_data="group-id-"+str(group.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data="group-faculty-"))
    return markup


class GroupPanel:
    def __init__(self, bot):
        self.bot = bot

    def choose_fac(self, message):
        self.bot.delete_message(
            message_id=message.message_id, chat_id=message.from_user.id)
        self.bot.send_message(
            message.from_user.id, "Выберите факультет:", reply_markup=faculties_markup())

    def choose_course(self, message):
        self.faculty = message.data.split('-')[-1]
        self.bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="group-back"+self.faculty, caption="group"))

    def choose_group(self, message):
        self.course = message.data.split('-')[-1]
        self.bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                   text='Виберіть группу:', reply_markup=group_markup(self.faculty, self.course, message))

    def call_save_group(self, message):
        save_group_user(message, message.data.split('-')[-1])
        self.bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                   text="Виберіть группу:", reply_markup=group_markup(self.faculty, self.course, message))

    def callback_handler(self, call):
        # -------> section choosing facutly <----------
        if call.data.startswith("group-faculty-"):
            self.choose_course(call)
        # -------> section choosing course <----------
        elif call.data.startswith('group-course-'):
            self.choose_group(call)
        elif call.data.startswith('group-id-'): self.call_save_group(call)
    
