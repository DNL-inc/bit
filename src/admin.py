from telebot import types
import telebot
from models.base import engine, Admin, register_fac, Faculty, register_group, delete_fac, edit_fac, get_fac
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from menu import get_main_menu, group_markup, course_markup_for_admin

Session = sessionmaker(bind=engine)
session = Session()


def faculties_markup(callback_for_back="backChooseFaculty", caption=""):
    markup = types.InlineKeyboardMarkup(row_width=1)
    faculites = session.query(Faculty).all()
    for faculty in faculites:
        markup.add(types.InlineKeyboardButton(text=faculty.title,
                                              callback_data="admin-faculty-"+str(faculty.id) + '-' + caption))
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


class FacultyPanel:
    def __init__(self, bot):
        self.bot = bot

    def actions_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        create_btn = types.InlineKeyboardButton(text="Создать факультет", callback_data="admin-faculty-add")
        edit_btn = types.InlineKeyboardButton(text='Изменить факультет', callback_data='admin-faculty-edit')
        delete_btn = types.InlineKeyboardButton(text="Удалить факультет", callback_data='admin-faculty-delete')
        markup.add(create_btn, edit_btn, delete_btn)
        return markup

    def get_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id, text="Выберите действия для группы:", reply_markup=self.actions_menu())

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
                msg.from_user.id, "Факультет уже есть такой", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Факультет создан", reply_markup=get_main_menu(msg, True))

    def execute_delete_faculty(self, msg):
        res = delete_fac(msg)

        self.bot.edit_message_text("Выбирете факультет, который нужно удалить", msg.from_user.id, msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'delete'))
        self.bot.send_message(
                msg.from_user.id, "Факультет удалет", reply_markup=get_main_menu(msg, True))

        
    def edit_faculty(self, msg):
        self.bot.edit_message_text("Выбирете факультет, который нужно изменить", msg.from_user.id, msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'edit'))
    
    def get_new_title_faculty(self, msg):
        self.fac_id = msg.data.split('-')[2]
        markup = types.ForceReply()
        message_id = self.bot.send_message(
            msg.from_user.id, "Напишите новое название факультета '{}':".format(get_fac(self.fac_id)), reply_markup=markup)
        self.bot.register_for_reply_by_message_id(
            message_id.message_id, callback=self.execute_edit_faculty)

    def execute_edit_faculty(self, msg):
        res = edit_fac(msg, self.fac_id)
        if res:
            self.bot.send_message(
                msg.from_user.id, "Факультет уже есть такой", reply_markup=get_main_menu(msg, True))
        else:
            self.bot.send_message(
                msg.from_user.id, "Факультет изменен", reply_markup=get_main_menu(msg, True))
        
    def delete_faculty(self, msg):
        self.bot.edit_message_text("Выбирете факультет, который нужно удалить", msg.from_user.id, msg.message.message_id, reply_markup=faculties_markup('admin-faculty-back', 'delete'))
        self.bot.send_message(
                msg.from_user.id, "Факультет изменен", reply_markup=get_main_menu(msg, True))

    def callback_handler(self, call):
        if call.data == 'admin-faculty':
            self.get_interface(call)
        elif call.data.endswith('add'):
            self.add_faculty(call)
        elif call.data == 'admin-faculty-delete':
            self.delete_faculty(call)
        elif call.data == 'admin-faculty-edit':
            self.edit_faculty(call)
        elif call.data == 'admin-faculty-back':
            self.get_interface(call)
        elif call.data.endswith('delete'):
            self.execute_delete_faculty(call)
        elif call.data.endswith('edit'):
            self.get_new_title_faculty(call)



class AdminPanel:
    def __init__(self, bot):
        self.bot = bot
        self.faculty_panel = FacultyPanel(self.bot)

    def callback_handler(self, call):
        if call.data.startswith('admin-faculty'):
            self.faculty_panel.callback_handler(call)
            

        # elif call.data.startswith('admin-group'):
        #     self.group_panel.callback_handler(call)
        # elif call.data.startswith('admin-event'):
        #     self.event_panel.callback_handler(call)

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

    
