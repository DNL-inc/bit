from telebot import types
from models.base import engine, Admin, register_fac
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from menu import get_main_menu

Session = sessionmaker(bind=engine)
session = Session()

def course_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    firstCourse = types.InlineKeyboardButton(text='1-й курс', callback_data="firstCourse_btn_admin") 
    secondCourse = types.InlineKeyboardButton(text='2-й курс', callback_data="secondCourse_btn_admin") 
    thirrdCourse = types.InlineKeyboardButton(text='3-й курс', callback_data="thirdCourse_btn_admin") 
    fourthCouse = types.InlineKeyboardButton(text='4-й курс', callback_data="fourthCourse_btn_admin") 
    fifthCourse = types.InlineKeyboardButton(text='5-й курс', callback_data="fifthCourse_btn_admin") 
    sixthCourse = types.InlineKeyboardButton(text='6-й курс', callback_data="sixthCourse_btn_admin")
    backButton = types.InlineKeyboardButton(text='Назад', callback_data="backChooseCourse")
    markup.add(firstCourse, secondCourse, thirrdCourse, fourthCouse, fifthCourse, sixthCourse, backButton)
    return markup

def menu_markup(admin):
    markup = types.InlineKeyboardMarkup(row_width=2)
    add_event_btn = types.InlineKeyboardButton(text='Создать событие', callback_data='add_event_btn')
    if admin.is_supreme:
        add_group_btn = types.InlineKeyboardButton(text='Создать группу', callback_data='add_group_btn')
        add_fac_btn = types.InlineKeyboardButton(text='Создать Факультет', callback_data='add_fac_btn')
        markup.add(add_group_btn, add_fac_btn)
    markup.add(add_event_btn)
    return markup

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot

    def get_admin(self, msg):
        admin = None
        try: 
            admin = session.query(Admin).filter(Admin.tele_id == msg.from_user.id).first()
        except OperationalError:
            return False
        else:
            self.admin = admin  
            return admin

    def get_menu(self, msg):
        self.bot.delete_message(message_id=msg.message_id, chat_id=msg.from_user.id) 
        admin = self.get_admin(msg)

        if not admin:
            return
        if admin.is_supreme or admin.group:
            self.bot.send_message(msg.from_user.id, "Меню:", reply_markup=menu_markup(admin))
        else: 
            self.bot.send_message(msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе")

    def choose_course_interface(self, msg):
        self.bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg.message.message_id, text='Виберіть курс:', reply_markup=course_markup())


    def call_create_fac(self, message):
        register_fac(message)
        self.bot.send_message(message.from_user.id, "Факультет создан", reply_markup=get_main_menu(message, True))


    def add_fac_interface(self, msg):
        markup = types.ForceReply()
        message_id = self.bot.send_message(msg.from_user.id, "Напишите название факультета (ФИТ):", reply_markup=markup)
        self.bot.register_for_reply_by_message_id(message_id.message_id, callback=self.call_create_fac)


    # def add_group_interface(self, msg):
    #     if msg.data == "firstCourse_btn_admin": 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-12):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
    #     elif msg.data == "secondCourse_btn_admin": 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-22):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
    #     elif msg.data == 'thirdCourse_btn_admin': 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-32):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
    #     elif msg.data == 'fourthCourse_btn_admin': 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-42):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
    #     elif msg.data == 'fifthCourse_btn_admin': 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-52):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
    #     elif msg.data == 'sixthCourse_btn_admin': 
    #         markup = types.ForceReply()
    #         message_id = self.bot.send_message(msg.from_user.id, text="Напишите название группы (ІПЗ-62):", reply_markup=markup)
    #         self.bot.register_for_reply_by_message_id(message_id, callback=)
