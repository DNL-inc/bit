from telebot import types
from models.base import engine, Admin, register_fac, Faculty, register_group
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from menu import get_main_menu, group_markup, course_markup_for_admin

Session = sessionmaker(bind=engine)
session = Session()


def faculties_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    faculites = session.query(Faculty).all()
    for faculty in faculites:
        markup.add(types.InlineKeyboardButton(text=faculty.title,
                                              callback_data="admin-faculty-"+str(faculty.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data="backChooseFaculty"))
    return markup


def menu_markup(admin):
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_event_btn = types.InlineKeyboardButton(
        text='Создать событие', callback_data='add_event_btn')
    if admin.is_supreme:
        add_group_btn = types.InlineKeyboardButton(
            text='Создать группу', callback_data='add_group_btn')
        add_fac_btn = types.InlineKeyboardButton(
            text='Создать Факультет', callback_data='add_fac_btn')
        markup.add(add_group_btn, add_fac_btn)
    markup.add(add_event_btn)
    return markup


class AdminPanel:
    def __init__(self, bot):
        self.bot = bot

    def get_admin(self, msg):
        admin = None
        try:
            admin = session.query(Admin).filter(
                Admin.tele_id == msg.from_user.id).first()
        except OperationalError:
            return False
        else:
            self.admin = admin
            return admin

    def get_menu(self, msg):
        self.bot.delete_message(
            message_id=msg.message_id, chat_id=msg.from_user.id)
        admin = self.get_admin(msg)

        if not admin:
            return
        if admin.is_supreme or admin.group:
            self.bot.send_message(msg.from_user.id, "Меню:",
                                  reply_markup=menu_markup(admin))
        else:
            self.bot.send_message(
                msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе")

    def choose_course_interface(self, msg):
        faculty_id = msg.data.split('-')[2]
        self.faculty = session.query(Faculty).filter(
            Faculty.id == faculty_id).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup_for_admin())

    def choose_faculty_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup())

    def call_create_fac(self, message):
        res = register_fac(message)
        if res:
            self.bot.send_message(
                message.from_user.id, "Факультет уже есть такой", reply_markup=get_main_menu(message, True))
        else:
            self.bot.send_message(
                message.from_user.id, "Факультет создан", reply_markup=get_main_menu(message, True))

    def add_fac_interface(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите название факультета (ФИТ):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.call_create_fac)

    def call_create_group(self, msg):
        res = register_group(msg, self.faculty, self.course)
        if res:
            self.bot.send_message(
                msg.from_user.id, "Группа уже есть такая", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Группа создана", reply_markup=get_main_menu(msg, True))

    def add_group_interface(self, msg):
        self.course = msg.data.split('-')[2]
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите название группы (ІПЗ-12):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.call_create_group)
