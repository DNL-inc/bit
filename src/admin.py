from telebot import types
import telebot
from models.base import engine, Admin, register_fac, Faculty, register_group, delete_fac, edit_fac, get_fac, delete_group, Group, edit_group, get_group, register_event, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from menu import get_main_menu, group_markup, course_markup, schedule_markup
import re

Session = sessionmaker(bind=engine)
session = Session()


def faculties_markup(callback_for_back="backChooseFaculty", caption=""):
    markup = types.InlineKeyboardMarkup(row_width=1)
    faculites = session.query(Faculty).all()
    for faculty in faculites:
        markup.add(types.InlineKeyboardButton(text=faculty.title,
                                              callback_data="admin-"+caption+"-"+str(faculty.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data=callback_for_back))
    return markup


def admin_menu_markup(admin):
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_event_btn = types.InlineKeyboardButton(
        text='Событие', callback_data='admin-event')
    if admin.is_supreme:
        add_group_btn = types.InlineKeyboardButton(
            text='Группа', callback_data='admin-group')
        add_fac_btn = types.InlineKeyboardButton(
            text='Факультет', callback_data='admin-faculty')
        markup.add(add_group_btn, add_fac_btn)
    markup.add(add_event_btn)
    return markup

def groups_markup(faculty_id, course, message, callback_for_back, callback):
    markup = types.InlineKeyboardMarkup(row_width=1)
    groups = session.query(Group).filter(
        Group.faculty == faculty_id, Group.course == course).all()
    for group in groups:
            markup.add(types.InlineKeyboardButton(
                text=group.title, callback_data=callback+"-"+str(group.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data=callback_for_back))
    return markup

class FacultyPanel:
    def __init__(self, bot):
        self.bot = bot

    def actions_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        create_btn = types.InlineKeyboardButton(
            text="Создать факультет", callback_data="admin-faculty-add")
        edit_btn = types.InlineKeyboardButton(
            text='Изменить факультет', callback_data='admin-faculty-edit')
        delete_btn = types.InlineKeyboardButton(
            text="Удалить факультет", callback_data='admin-faculty-delete')
        markup.add(create_btn, edit_btn, delete_btn)
        return markup

    def get_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите действия для факультета:", reply_markup=self.actions_menu())

    def add_faculty(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите название факультета (ФИТ):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_add_faculty)

    def execute_add_faculty(self, msg):
        res = register_fac(msg)
        if res:
            self.bot.send_message(
                msg.from_user.id, "Факультет создан", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Факультет уже есть такой", reply_markup=get_main_menu(msg, True))

    def execute_delete_faculty(self, msg):
        res = delete_fac(msg)

        self.bot.edit_message_text("Выбирете факультет, который нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'faculty-delete-id'))
        self.bot.send_message(
            msg.from_user.id, "Факультет удалет", reply_markup=get_main_menu(msg, True))

    def edit_faculty(self, msg):
        self.bot.edit_message_text("Выбирете факультет, который нужно изменить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'faculty-edit-id'))

    def get_new_title_faculty(self, msg):
        self.fac_id = msg.data.split('-')[-1]
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите новое название факультета '{}':".format(get_fac(self.fac_id)), reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_edit_faculty)

    def execute_edit_faculty(self, msg):
        res = edit_fac(msg, self.fac_id)
        if res:
            self.bot.send_message(
                msg.from_user.id, "Факультет изменен", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Факультет уже есть такой", reply_markup=get_main_menu(msg, True))

    def delete_faculty(self, msg):
        self.bot.edit_message_text("Выбирете факультет, который нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'faculty-delete-id'))
        self.bot.send_message(
            msg.from_user.id, "Факультет изменен", reply_markup=get_main_menu(msg, True))

    def callback_handler(self, call):
        if call.data == 'admin-faculty':
            self.get_interface(call)
        elif call.data.startswith('admin-faculty-delete-id'):
            self.execute_delete_faculty(call)
        elif call.data.startswith('admin-faculty-edit-id'):
            self.get_new_title_faculty(call)
        elif call.data.endswith('add'):
            self.add_faculty(call)
        elif call.data == 'admin-faculty-delete':
            self.delete_faculty(call)
        elif call.data == 'admin-faculty-edit':
            self.edit_faculty(call)
        elif call.data == 'admin-faculty-back':
            self.get_interface(call)
        

class GroupPanel:
    def __init__(self, bot):
        self.bot = bot

    def actions_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        create_btn = types.InlineKeyboardButton(
            text="Создать группу", callback_data="admin-group-add")
        edit_btn = types.InlineKeyboardButton(
            text='Изменить группу', callback_data='admin-group-edit')
        delete_btn = types.InlineKeyboardButton(
            text="Удалить группу", callback_data='admin-group-delete')
        markup.add(create_btn, edit_btn, delete_btn)
        return markup

    def get_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите действия для группы:", reply_markup=self.actions_menu())

    def choose_faculty_add_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-add-id'))

    def add_group(self, msg):
        self.course = msg.data.split('-')[-1]
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите название группы (ІПЗ-12):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_add_group)

    def choose_course_add_interface(self, msg):
        faculty_id = msg.data.split('-')[-1]
        self.faculty = session.query(Faculty).filter(
            Faculty.id == faculty_id).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-add", admin="admin-group-add-course"))

    def execute_add_group(self, msg):
        res = register_group(msg, self.faculty, self.course)
        if res:
            self.bot.send_message(
                msg.from_user.id, "Группа уже есть такоя", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Группа создана", reply_markup=get_main_menu(msg, True))

    def choose_faculty_delete_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-delete-id'))

    def choose_course_delete_interface(self, msg):
        faculty_id = msg.data.split('-')[-1]
        self.faculty = session.query(Faculty).filter(
            Faculty.id == faculty_id).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", admin="admin-group-delete-course"))

    def choose_group_delete_interface(self, msg):
        self.course = msg.data.split('-')[-1]
        self.bot.edit_message_text("Выбирете группу, которую нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=groups_markup(self.faculty.id, self.course, msg, 'admin-group-delete-id', "admin-group-delete-choose"))

    def execute_delete_group(self, msg): 
        res = delete_group(msg)

        self.bot.edit_message_text("Выбирете группу, которую нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=groups_markup(self.faculty.id, self.course, msg, 'admin-group-delete-id', "admin-group-delete-choose"))

        self.bot.send_message(
            msg.from_user.id, "Группа удалена", reply_markup=get_main_menu(msg, True))


    def edit_group(self, msg):
        self.bot.edit_message_text("Выбирете группу, которую нужно изменить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-group-back', 'group-edit-id'))

    def choose_faculty_edit_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-edit-id'))

    def choose_course_edit_interface(self, msg):
        faculty_id = msg.data.split('-')[-1]
        self.faculty = session.query(Faculty).filter(
            Faculty.id == faculty_id).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", admin="admin-group-edit-course"))

    def choose_group_edit_interface(self, msg):
        self.course = msg.data.split('-')[-1]
        self.bot.edit_message_text("Выбирете группу, которую нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=groups_markup(self.faculty.id, self.course, msg, 'admin-group-edit-id', "admin-group-edit-choose"))


    def get_new_title_group(self, msg):
        self.group_id = msg.data.split('-')[-1]
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите новое название группы '{}':".format(get_group(self.group_id)), reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_edit_group)

    def execute_edit_group(self, msg):
        res = edit_group(msg, self.group_id)
        if not res:
            self.bot.send_message(
                msg.from_user.id, "Группа уже есть такая", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Группа изменена", reply_markup=get_main_menu(msg, True))

    def delete_group(self, msg):
        self.bot.edit_message_text("Выбирете группу, которую нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-group-back', 'group-delete-id'))

    def callback_handler(self, call):
        if call.data == 'admin-group':
            self.get_interface(call)
        elif call.data.startswith('admin-group-add-id'):
            self.choose_course_add_interface(call)
        elif call.data.startswith('admin-group-delete-id'):
            self.choose_course_delete_interface(call)
        elif call.data.startswith('admin-group-edit-id'):
            self.choose_course_edit_interface(call)
        elif call.data.startswith('admin-group-delete-choose'):
            self.execute_delete_group(call)
        elif call.data.startswith('admin-group-edit-choose'):
            self.get_new_title_group(call)
        elif call.data.startswith('admin-group-add-course'):
            self.add_group(call)
        elif call.data.startswith('admin-group-delete-course'):
            self.choose_group_delete_interface(call)
        elif call.data.startswith('admin-group-edit-course'):
            self.choose_group_edit_interface(call)
        elif call.data == 'admin-group-back':
            self.get_interface(call)
        elif call.data.startswith('admin-group-add'):
            self.choose_faculty_add_interface(call)
        elif call.data == 'admin-group-delete':
            self.delete_group(call)
        elif call.data == 'admin-group-edit':
            self.edit_group(call)
        elif call.data == 'admin-group-back':
            self.get_interface(call)

class EventPanel:
    def __init__(self, bot):
        self.bot = bot 

    def actions_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        create_btn = types.InlineKeyboardButton(
            text="Создать события", callback_data="admin-event-add")
        edit_btn = types.InlineKeyboardButton(
            text='Изменить события', callback_data='admin-event-edit')
        delete_btn = types.InlineKeyboardButton(
            text="Удалить события", callback_data='admin-event-delete')
        markup.add(create_btn, edit_btn, delete_btn)
        return markup

    def get_interface(self, msg):
        user = session.query(User).filter(User.tele_id == msg.from_user.id).first()
        admin = session.query(Admin).filter(Admin.tele_id == msg.from_user.id).first()
        if admin.is_supreme:
            if user.group:
                self.bot.send_message(msg.from_user.id, "У вас не выбранна группа. Сделать это можно в главном меню в секции 'Группа'")
                return False
        elif admin.group:
            self.bot.send_message(msg.from_user.id, "Вы можете редактировать события только в позволеной вам группе")
        else:
            self.bot.send_message(msg.from_user.id, "Кажеться, вы не СУПРИМ или вы просто не можете создавать ивенты")
            return False
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите действия для события:", reply_markup=self.actions_menu())

    def choose_schedule(self, msg):
        self.bot.edit_message_text("Выберите день:", chat_id=msg.from_user.id, message_id=msg.message.message_id, reply_markup=schedule_markup(caption='admin-event', back="admin-event"))

    def pick_up_time(self, msg):
        try: self.day
        except AttributeError: self.day = msg.data.split('_')[-1]
        markup = types.ForceReply()
        message_id = self.bot.send_message(text="Напишите время в формате 24-часов (9:00):", chat_id=msg.from_user.id, reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.check_time_event)

    def get_title_event(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(msg.from_user.id, "Напишите названия события (Выш мат):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(message_id.message_id, callback=self.confirm_add)

    def check_time_event(self, msg):
        res = re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', msg.text)
        if not res:
            self.pick_up_time(msg)
        else:
            self.time = msg.text
            self.get_title_event(msg)

    def confirm_add(self, msg):
        self.title = msg.text
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Создать", callback_data="admin-event-add-confirm"), types.InlineKeyboardButton("Отмена", callback_data="admin-event"))
        self.bot.send_message(msg.from_user.id, "Cоздать {} на {} в {}, подтвердить?".format(self.title, self.time, self.day), reply_markup=markup)

    def add_event(self, msg):
        self.bot.delete_message(msg.from_user.id, msg.message.message_id)
        res = register_event(msg, self.title, self.time, self.day)
        if not res:
            self.bot.send_message(msg.from_user.id, "Что-то пошло не так!", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(msg.from_user.id, "Событие созданно!", reply_markup=get_main_menu(msg, True))


    def callback_handler(self, call):
        if call.data == 'admin-event':
            self.get_interface(call)
        elif call.data == 'admin-event-add':
            self.choose_schedule(call)
        elif call.data.startswith('admin-event-schedule'):
            self.pick_up_time(call)
        elif call.data == 'admin-event-edit':
            self.choose_schedule(call)
        elif call.data == 'admin-event-delete':
            self.choose_schedule(call)
        elif call.data == 'admin-event-add-confirm':
            self.add_event(call)

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot
        self.faculty_panel = FacultyPanel(self.bot)
        self.group_panel = GroupPanel(self.bot)
        self.event_panel = EventPanel(self.bot)

    def callback_handler(self, call):
        if call.data.startswith('admin-faculty'):
            self.faculty_panel.callback_handler(call)
        elif call.data.startswith('admin-group'):
            self.group_panel.callback_handler(call)
        elif call.data.startswith('admin-event'):
            self.event_panel.callback_handler(call)

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
                                  reply_markup=admin_menu_markup(admin))
        else:
            self.bot.send_message(
                msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе") 