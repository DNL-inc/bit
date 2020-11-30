import re

import telebot
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from telebot import types

from menu import course_markup, get_main_menu, schedule_markup
from models.base import (Admin, Event, Faculty, Group, User, delete_event,
                         delete_fac, delete_group, edit_fac, edit_group,
                         engine, get_fac, get_group, get_user, register_event,
                         register_fac, register_group, edit_event, add_admin, delete_admin)
from record import Record
from group import GroupPanel
record = Record()

from math import ceil

Session = sessionmaker(bind=engine)
session = Session()

def group_markup(faculty_id, course, message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    user = session.query(User).filter(
        User.tele_id == message.from_user.id).first()
    groups = session.query(Group).filter(
        Group.faculty == faculty_id, Group.course == course).all()
    for group in groups:
        markup.add(types.InlineKeyboardButton(
                text=group.title, callback_data="admin-manage-admin-group-id-"+str(group.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data="admin-manage-admin-course-"+faculty_id))
    return markup

def faculties_markup(callback_for_back="backChooseFaculty", caption=""):
    markup = types.InlineKeyboardMarkup(row_width=1)
    faculites = session.query(Faculty).all()
    for faculty in faculites:
        markup.add(types.InlineKeyboardButton(text=faculty.title,
                                              callback_data="admin-"+caption+"-"+str(faculty.id)))
    markup.add(types.InlineKeyboardButton(
        text='Назад', callback_data=callback_for_back))
    return markup

def is_callback(call):
    try: call.data
    except AttributeError:
        return False
    return True

def admin_menu_markup(admin):
    markup = types.InlineKeyboardMarkup(row_width=2)
    event_btn = types.InlineKeyboardButton(
        text='Событие', callback_data='admin-event')
    if admin.is_supreme:
        group_btn = types.InlineKeyboardButton(
            text='Группа', callback_data='admin-group')
        fac_btn = types.InlineKeyboardButton(
            text='Факультет', callback_data='admin-faculty')
        admin_btn = types.InlineKeyboardButton('Админы', callback_data='admin-manage-admin')
        markup.add(group_btn, fac_btn, admin_btn, row_width=2)
    markup.add(event_btn, row_width=2)
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


def user_markup(caption, page, limit):
    print(page)
    page = int(page)
    users_len = len(session.query(User).all())

    users = session.query(User).limit(limit).offset(page*limit).all()
    markup = types.InlineKeyboardMarkup(row_width=1)
    for user in users:  
        text = ""
        if user.firstname: text += user.firstname
        if user.lastname: text += " " + user.lastname
        if user.is_admin:
            markup.add(types.InlineKeyboardButton(text=text+" ✅", callback_data=caption+"-admin-id-"+str(user.id)))
        else:
            markup.add(types.InlineKeyboardButton(text=text, callback_data=caption+"-user-id-"+str(user.id)))
    if int(page) > 0 and int(page) + 1 < ceil(users_len / limit):
        markup.add(types.InlineKeyboardButton(text='Назад', callback_data=caption+'-page-'+str(page-1)), types.InlineKeyboardButton(text='Вперед', callback_data=caption+'-page-'+str(page+1)), row_width=2)
    elif int(page) == 0:
        markup.add(types.InlineKeyboardButton(text='Вперед', callback_data=caption+'-page-'+str(page+1)))
    elif int(page) + 1 >= ceil(users_len / limit):
        markup.add(types.InlineKeyboardButton(text='Назад', callback_data=caption+'-page-'+str(page-1)))
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
        record.create(msg.from_user.id, Group().to_dict())
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-add-id'))

    def add_group(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'course') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'course', msg.data.split('-')[-1]) 
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите название группы (ІПЗ-12):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_add_group)

    def choose_course_add_interface(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'faculty') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'faculty', msg.data.split('-')[-1]) 
        self.faculty = session.query(Faculty).filter(
            Faculty.id == record.get_value(msg.from_user.id, 'faculty')).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-add", caption="admin-group-add-course"))

    def execute_add_group(self, msg):
        record.set_value(msg.from_user.id, 'title', msg.text)
        data = record.get(msg.from_user.id)
        res = register_group(data['title'], data['faculty'], data['course'])
        if not res:
            self.bot.send_message(
                msg.from_user.id, "Такая группа уже существует", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Группа создана", reply_markup=get_main_menu(msg, True))

    def choose_faculty_delete_interface(self, msg):
        record.create(msg.from_user.id, Group().to_dict())
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-delete-id'))

    def choose_course_delete_interface(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'faculty') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'faculty', msg.data.split('-')[-1]) 
        self.faculty = session.query(Faculty).filter(
            Faculty.id == faculty_id).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", caption="admin-group-delete-course"))

    def choose_group_delete_interface(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'course') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'course', msg.data.split('-')[-1]) 
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
        record.create(msg.from_user.id, Group().to_dict())
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите факультет:", reply_markup=faculties_markup(callback_for_back='admin-group-back', caption='group-edit-id'))

    def choose_course_edit_interface(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'faculty') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'faculty', msg.data.split('-')[-1]) 
        self.faculty = session.query(Faculty).filter(
            Faculty.id == record.set_value(msg.from_user.id, 'faculty', msg.data.split('-')[-1])).first()
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберіть курс:', reply_markup=course_markup(callback_for_back="admin-group-delete", caption="admin-group-edit-course"))

    def choose_group_edit_interface(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'course') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'course', msg.data.split('-')[-1])
        self.bot.edit_message_text("Выбирете группу, которую нужно удалить", msg.from_user.id,
                                   msg.message.message_id, reply_markup=groups_markup(self.faculty.id, record.set_value(msg.from_user.id, 'course', msg.data.split('-')[-1]), msg, 'admin-group-edit-id', "admin-group-edit-choose"))

    def get_new_title_group(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'id') != msg.data.split('-')[-1]:
                record.set_value(msg.from_user.id, 'id', msg.data.split('-')[-1]) 
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите новое название группы '{}':".format(get_group(record.set_value(msg.from_user.id, 'id', msg.data.split('-')[-1]))), reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_edit_group)

    def execute_edit_group(self, msg):
        record.set_value(msg.from_user.id, 'title', msg.text)
        data = record.get(msg.from_user.id)
        res = edit_group(data['title'], data['id'])
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
            pass
        else:
            self.bot.send_message(
                msg.from_user.id, "Кажеться, вы не СУПРИМ или вы просто не можете создавать события")
            return False
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text="Выберите действия для события:", reply_markup=self.actions_menu())

    def choose_schedule(self, msg):
        record.create(msg.from_user.id, Event().to_dict())
        self.bot.edit_message_text("Выберите день:", chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   reply_markup=schedule_markup(caption=msg.data+'-schedule', back="admin-event"))

    def pick_up_time(self, msg):
        if is_callback(msg):
            if record.get_value(msg.from_user.id, 'day') != msg.data.split('_')[-1]:
                record.set_value(msg.from_user.id, 'day', msg.data.split('_')[-1]) 
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
                record.set_value(msg.from_user.id, 'time_start', msg.text)
                self.get_title_event(msg)
        else:
            if not res:
                self.edit_time(msg)
            else:
                record.set_value(msg.from_user.id, 'time_start', msg.text)
                self.confirm_edit(msg, changes="time")

    def confirm_add(self, msg):
        record.set_value(msg.from_user.id, 'title', msg.text)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Создать", callback_data="admin-event-add-confirm"),
                   types.InlineKeyboardButton("Отмена", callback_data="admin-event-cancel"))
        data = record.get(msg.from_user.id)
        self.bot.send_message(msg.from_user.id, "Cоздать {} на {} в {}, подтвердить?".format(data['title'], data['day'], data['time_start']), reply_markup=markup)

    def add_event(self, msg):
        self.bot.delete_message(msg.from_user.id, msg.message.message_id)
        data = record.get(msg.from_user.id)
        res = register_event(msg, data['title'], data['time_start'], data['day'])
        if not res:
            self.bot.send_message(
                msg.from_user.id, "Что-то пошло не так!", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Событие созданно!", reply_markup=get_main_menu(msg, True))

        record.delete(msg.from_user.id)

    def choose_event(self, msg):
        record.create(msg.from_user.id, Event().to_dict())
        if is_callback(msg):
                if record.get_value(msg.from_user.id, 'day') != msg.data.split('_')[-1]:
                    record.set_value(msg.from_user.id, 'day', msg.data.split('_')[-1]) 
        day = record.get_value(msg.from_user.id, 'day')
                
        markup = types.InlineKeyboardMarkup(row_width=1)
        user = get_user(msg)
        self.events = session.query(Event).filter(
            Event.group == user.group).filter(Event.day == day).all()
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
        id = msg.data.split('-')[-1]
        event = session.query(Event).filter(Event.id == id).first()
        record.update(msg.from_user.id, event.to_dict())
        day = event.day
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
        res = edit_event(msg, record.get(msg.from_user.id))

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
            record.set_value(msg.from_user.id, 'title', msg.text)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(types.InlineKeyboardButton("Изменить", callback_data="admin-event-edit-confirm"),
                   types.InlineKeyboardButton("Отмена", callback_data="admin-event-cancel"))
        data = record.get(msg.from_user.id)
        self.bot.send_message(msg.from_user.id, "Изменить {} на {} в {}, подтвердить?".format(
                data['title'], data['time_start'], data['day']), reply_markup=markup)

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

class ManageAdmin:
    def __init__(self, bot):
        self.bot = bot
        self.group_panel = GroupPanel(self.bot)
        self.limit_for_buttons = 10
        
    def callback_handler(self, call):
        if call.data == 'admin-manage-admin':
            self.get_interface(call)
        elif call.data.startswith('admin-manage-admin-page-'):
            self.get_users(call)
        elif call.data.startswith('admin-manage-admin-user-id'):
            self.change_admin(call)
        elif call.data.startswith('admin-manage-admin-admin-id'):
            self.delete_admin(call)
        elif call.data.startswith('admin-manage-admin-faculty'):
            self.choose_course(call)
        elif call.data.startswith('admin-manage-admin-course'):
            self.choose_group(call)
        elif call.data.startswith('admin-manage-admin-group'):
            self.create_admin(call)
            

    def get_interface(self, msg):
        record.create(msg.from_user.id, dict({'page': 0, 'user_id': None, 'faculty': None, 'course': None}))
        user = session.query(User).filter(
            User.tele_id == msg.from_user.id).first()
        admin = session.query(Admin).filter(
            Admin.tele_id == msg.from_user.id).first()
        if admin.is_supreme:
            self.bot.send_message(text="Чтобы назначить/убрать админа нужно лишь нажать на название человека", chat_id=msg.from_user.id, reply_markup=user_markup('admin-manage-admin', 0, self.limit_for_buttons))
        else:
            self.bot.send_message(
                msg.from_user.id, "Кажеться, вы не СУПРИМ", reply_markup=get_main_menu(call, True))
            return False

    def get_users(self, msg):
        record.set_value(msg.from_user.id, 'page', msg.data.split('-')[-1])
        self.bot.edit_message_text("Чтобы назначить/убрать админа нужно лишь нажать на название человека", msg.from_user.id, msg.message.message_id, reply_markup=user_markup('admin-manage-admin', msg.data.split('-')[-1], self.limit_for_buttons))

    def change_admin(self, msg):
        record.set_value(msg.from_user.id, 'user_id', msg.data.split('-')[-1])
        try: msg.message_id
        except AttributeError: 
            self.bot.edit_message_text( 
                chat_id=msg.from_user.id, message_id=msg.message.message_id, text="Выберите факультет за которым он будет редактировать:", reply_markup=faculties_markup('admin-manage-admin-page', 'manage-admin-faculty-id'))
        else:
            self.bot.delete_message(
                message_id=msg.message_id, chat_id=msg.from_user.id)
            self.bot.send_message(
                msg.from_user.id, "Выберите факультет за которым он будет редактировать:", reply_markup=faculties_markup('admin-manage-admin-page', 'manage-admin-faculty-id')) 

    def choose_course(self, msg):
        user_id = record.get_value(msg.from_user.id, 'user_id')
        record.set_value(msg.from_user.id, 'faculty', msg.data.split('-')[-1])
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберите курс:', reply_markup=course_markup(callback_for_back="admin-manage-admin-user-id-"+str(user_id), caption="admin-manage-admin"))

    def choose_group(self, msg):
        record.set_value(msg.from_user.id, 'course', msg.data.split('-')[-1])
        faculty = record.get_value(msg.from_user.id, 'faculty')
        course = record.get_value(msg.from_user.id, 'course')
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id,
                                   text='Виберите группу:', reply_markup=group_markup(faculty, course, msg))

    def create_admin(self, msg):
        record.set_value(msg.from_user.id, 'group', msg.data.split('-')[-1])
        data = record.get(msg.from_user.id)

        res = add_admin(data)
        if res:
            self.bot.send_message(chat_id=msg.from_user.id, text='Админ добавлен!', reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(chat_id=msg.from_user.id, text='Что-то пошло не так', reply_markup=get_main_menu(msg, True))

        record.delete(msg.from_user.id)

    def delete_admin(self, msg):
        res = delete_admin(msg.data.split('-')[-1])
        if res:
            self.bot.edit_message_text(chat_id=msg.from_user.id, text='Админ удален!', message_id=msg.message.message_id, reply_markup=user_markup('admin-manage-admin', 0, self.limit_for_buttons))
        else:
            self.bot.edit_message_text(chat_id=msg.from_user.id, text='Что-то пошло не так', message_id=msg.message.message_id, reply_markup=user_markup('admin-manage-admin', 0, self.limit_for_buttons))

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot
        self.faculty_panel = FacultyPanel(self.bot)
        self.group_panel = GroupPanel(self.bot)
        self.event_panel = EventPanel(self.bot)
        self.manage_admin = ManageAdmin(self.bot)

    def callback_handler(self, call):
        if call.data.startswith('admin-faculty'):
            self.faculty_panel.callback_handler(call)
        elif call.data.startswith('admin-group'):
            self.group_panel.callback_handler(call)
        elif call.data.startswith('admin-event'):
            self.event_panel.callback_handler(call)
        elif call.data.startswith('admin-manage-admin'):
            self.manage_admin.callback_handler(call)

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
        user = None
        if admin:
            user = session.query(User).filter(User.tele_id == admin.tele_id).first()

        if not admin or not user:
            return
        if admin.is_supreme or user.group:
            self.bot.send_message(msg.from_user.id, "Меню:",
                                  reply_markup=admin_menu_markup(admin))
        else:
            self.bot.send_message(
                msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе")


