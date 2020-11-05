from telebot import types
from models.base import engine, Admin
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

Session = sessionmaker(bind=engine)
session = Session()

class AdminPanel:
    def __init__(self, bot):
        self.bot = bot

    def _get_admin_tele_id(self, msg):
        admin = None
        try: 
            admin = session.query(Admin).filter(Admin.tele_id == msg.from_user.id).first()
        except OperationalError:
            return False
        else:
            self.admin = admin  
            return admin

    def get_menu(self, msg): 
        admin = self._get_admin_tele_id(msg)

        markup = types.InlineKeyboardMarkup(row_width=2)

        if admin.is_supreme or admin.has_group:
            add_event_btn = types.InlineKeyboardButton(text='Создать событие', callback_data='add_event_btn')
            if admin.is_supreme:
                add_group_btn = types.InlineKeyboardButton(text='Создать группу', callback_data='add_group_btn')
                markup.add(add_group_btn)
            markup.add(add_event_btn)

            self.bot.send_message(msg.from_user.id, "Меню:", reply_markup=markup)
        else: 
            self.bot.send_message(msg.from_user.id, "Чтобы вносить изменения вам нужно принадлежать какой-то группе")

