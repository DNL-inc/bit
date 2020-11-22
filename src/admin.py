import re

import telebot
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from telebot import types

from menu import course_markup, get_main_menu, schedule_markup
from models.base import (Admin, Event, Faculty, Group, User, delete_event,
                         delete_fac, delete_group, edit_fac, edit_group,
                         engine, get_fac, get_group, get_user, register_event,
                         register_fac, register_group, edit_event)

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
                msg.from_user.id, "Такой факультет уже существует", reply_markup=get_main_menu(msg, True))

    def execute_delete_faculty(self, msg):
        res = delete_fac(msg)

        self.bot.edit_message_text("Выбирете факультет, который нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'faculty-delete-id'))
        self.bot.send_message(
            msg.from_user.id, "Факультет удален", reply_markup=get_main_menu(msg, True))

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
                msg.from_user.id, "Такой факультет уже существует", reply_markup=get_main_menu(msg, True))

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
                                   text='Виберите курс:', reply_markup=course_markup(callback_for_back="admin-group-add", admin="admin-group-add-course"))

    def execute_add_group(self, msg):
        res = register_group(msg, self.faculty, self.course)
        if not res:
            self.bot.send_message(
                msg.from_user.id, "Такая группа уже существует", reply_markup=get_main_menu(msg, True))
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
                                   text='Виберите курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", admin="admin-group-delete-course"))

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
                                   text='Виберите курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", admin="admin-group-edit-course"))

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
                msg.from_user.id, "Такая группа уже существует", reply_markup=get_main_menu(msg, True))
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
            text="Создать событие", callback_data="admin-event-add")
        edit_btn = types.InlineKeyboardButton(
            text='Изменить событие', callback_data='admin-event-edit')
        delete_btn = types.InlineKeyboardButton(
            text="Удалить событие", callback_data='admin-event-delete')
        markup.add(create_btn, edit_btn, delete_btn)
        return markup

    def get_interface(self, msg):
        user = session.query(User).filter(
            User.tele_id == msg.from_user.id).first()
        admin = session.query(Admin).filter(
            Admin.tele_id == msg.from_user.id).first()
        if admin.is_supreme:
            if not user.group:  # supreme can't have group that's why we check in user
                self.bot.send_message(
                    msg.from_user.id, "У вас не выбранна группа. Сделать это можно в главном меню в секции 'Группа'")
                return False
        elif admin.group:
            self.bot.send_message(
                msg.from_user.id, "Вы можете редактировать события только в позволеной вам группе")
        else:
            self.bot.send_message(
                msg.from_user.id, "Кажеться, вы не СУПРИМ или вы просто не можете создавать события")
            return False
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите действия для события:", reply_markup=self.actions_menu())

    def choose_schedule(self, msg):
        self.bot.edit_message_text("Выберите день:", chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   reply_markup=schedule_markup(caption=msg.data+'-schedule', back="admin-event"))

    def pick_up_time(self, msg):
        try:
            self.day
        except AttributeError:
            self.day = msg.data.split('_')[-1]
        markup = types.ForceReply()
        self.add = True
        message_id = self.bot.send_message(
            text="Напишите время в формате 24-часов (9:00):", chat_id=msg.from_user.id, reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.check_time_event)

    def get_title_event(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Введите название пары и ссылку на нее в таком формате: [название пары](ссылка на пару)", reply_markup=markup, parse_mode="HTML")
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.confirm_add)

    def check_time_event(self, msg):
        res = re.match('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', msg.text)
        if self.add:
            if not res:
                self.pick_up_time(msg)
            else:
                self.time = msg.text
                self.get_title_event(msg)
        else:
            if not res:
                self.edit_time(msg)
            else:
                self.time = msg.text
                self.confirm_edit(msg, changes="time")

    def confirm_add(self, msg):
        self.title = msg.text
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Создать", callback_data="admin-event-add-confirm"),
                   types.InlineKeyboardButton("Отмена", callback_data="admin-event-cancel"))
        self.bot.send_message(msg.from_user.id, "Cоздать {} на {} в {}, подтвердить?".format(
            self.title, self.time, self.day), reply_markup=markup)

    def add_event(self, msg):
        self.bot.delete_message(msg.from_user.id, msg.message.message_id)
        res = register_event(msg, self.title, self.time, self.day)
        if not res:
            self.bot.send_message(
                msg.from_user.id, "Что-то пошло не так!", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Событие созданно!", reply_markup=get_main_menu(msg, True))

    def choose_event(self, msg):
        try:
            self.day
        except AttributeError:
            self.day = msg.data.split('_')[-1]

        if self.day == "admin-event-delete-schedule" or self.day  == 'admin-event-edit-schedule': pass
        elif self.day != msg.data.split('_')[-1]: self.day = msg.data.split('_')[-1]
                
        markup = types.InlineKeyboardMarkup(row_width=1)
        user = get_user(msg)
        self.events = session.query(Event).filter(
            Event.group == user.group).filter(Event.day == self.day).all()
        for event in self.events:
            title = event.title.split('[')[-1].split(']')[0]
            self.time_start = event.time_start.strftime('%H:%M')
            text = 'Начало в {} {}'.format(self.time_start, title)
            markup.add(types.InlineKeyboardButton(
                text, callback_data="-".join(msg.data.split('-')[:3]) + '-id-'+str(event.id)))
        markup.add(types.InlineKeyboardButton(
            "Назад", callback_data="-".join(msg.data.split('-')[:3])))
        self.bot.edit_message_text(
            'Выберите событие:', msg.from_user.id, msg.message.message_id, reply_markup=markup)

    def confirm_delete(self, msg):
        event_id = msg.data.split('-')[-1]
        for event in self.events:
            if event.id == int(event_id):
                self.event = event
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Удалить", callback_data="admin-event-delete-confirm"),
                   types.InlineKeyboardButton("Отмена", callback_data="admin-event-cancel"))
        self.bot.send_message(msg.from_user.id, "Удалить {} на {} в {}, подтвердить?".format(
            self.event.title, self.time_start, self.event.day), reply_markup=markup)

    def delete_event(self, msg):
        self.bot.delete_message(msg.from_user.id, msg.message.message_id)
        res = delete_event(msg, self.event)

        if res:
            self.bot.send_message(
                msg.from_user.id, "Событие удалено", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Что-то пошло не так!", reply_markup=get_main_menu(msg, True))

    def choose_time_or_title_to_edit(self, msg):
        self.event_id = msg.data.split('-')[-1]
        day = session.query(Event).filter(
            Event.id == int(self.event_id)).first().day
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(
                "Время", callback_data="admin-event-edit-time"),
            types.InlineKeyboardButton(
                "Название", callback_data="admin-event-edit-title"),
            types.InlineKeyboardButton("Назад", callback_data="admin-event-edit-schedule_"+day))
        self.bot.edit_message_text(
            "Что вы хотите изменить:", msg.from_user.id, msg.message.message_id, reply_markup=markup)

    def edit_time(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            text="Напишите время в формате 24-часов (9:00):", chat_id=msg.from_user.id, reply_markup=markup)
        self.add = False
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.check_time_event)

    def edit_event(self, msg):
        self.bot.delete_message(msg.from_user.id, msg.message.message_id)
        res = edit_event(msg, self.changes)

        if res:
            self.bot.send_message(
                msg.from_user.id, "Событие изменено", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Что-то пошло не так!", reply_markup=get_main_menu(msg, True))

    def set_new_titile(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Введите название пары и ссылку на нее в таком формате: [название пары](ссылка на пару)", reply_markup=markup, parse_mode="HTML")
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.confirm_edit)

    def confirm_edit(self, msg, changes='title'):
        if changes == 'title':
            self.title = msg.text
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Изменить", callback_data="admin-event-edit-confirm"),
                   types.InlineKeyboardButton("Отмена", callback_data="admin-event-cancel"))
        event = session.query(Event).filter(Event.id == self.event_id).first()
        self.changes = dict()
        self.changes['id'] = event.id
        if changes == 'time':
            self.bot.send_message(msg.from_user.id, "Изменить {} на {} в {}, подтвердить?".format(
                event.title, self.time, event.day), reply_markup=markup)
            self.changes[changes] = self.time
        elif changes == 'title':
            self.bot.send_message(msg.from_user.id, "Изменить {} на {} в {}, подтвердить?".format(
                self.title, event.time_start, event.day), reply_markup=markup)
            self.changes[changes] = self.title
        else:
            self.bot.send_message(msg.from_user.id, "Изменить {} на {} в {}, подтвердить?".format(
                self.title, self.time, event.day), reply_markup=markup)
            self.changes['time'] = self.time
            self.changes['title'] = self.title

    def cancel_action(self, msg):
        self.bot.send_message(msg.from_user.id, "Отмена",
                              reply_markup=get_main_menu(msg, True))

    def callback_handler(self, call):
        if call.data == 'admin-event':
            self.get_interface(call)
        elif call.data == 'admin-event-add':
            self.choose_schedule(call)
        elif call.data == 'admin-event-edit':
            self.choose_schedule(call)
        elif call.data == 'admin-event-delete':
            self.choose_schedule(call)
        elif call.data == 'admin-event-add-confirm':
            self.add_event(call)
        elif call.data == 'admin-event-edit-time':
            self.edit_time(call)
        elif call.data == 'admin-event-edit-title':
            self.set_new_titile(call)
        elif call.data == 'admin-event-delete-confirm':
            self.delete_event(call)
        elif call.data == 'admin-event-edit-confirm':
            self.edit_event(call)
        elif call.data == 'admin-event-cancel':
            self.cancel_action(call)
        elif call.data.startswith('admin-event-add-schedule'):
            self.pick_up_time(call)
        elif call.data.startswith('admin-event-delete-schedule'):
            self.choose_event(call)
        elif call.data.startswith('admin-event-edit-schedule'):
            self.choose_event(call)
        elif call.data.startswith('admin-event-delete-id'):
            self.confirm_delete(call)
        elif call.data.startswith('admin-event-edit-id'):
            self.choose_time_or_title_to_edit(call)


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
        user = session.query(User).filter(User.tele_id == admin.tele_id).first()

        if not admin:
            return
        if admin.is_supreme or user.group:
            self.bot.send_message(msg.from_user.id, "Меню:",
                                  reply_markup=admin_menu_markup(admin))
        else:
            self.bot.send_message(
                msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе")


