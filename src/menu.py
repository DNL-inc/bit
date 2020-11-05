
from telebot import types

def get_main_menu(message, is_admin):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    schedule_item = types.KeyboardButton('Рaспиcание')
    group_item = types.KeyboardButton('Група')
    if is_admin:
        admin_item = types.KeyboardButton('Админиcтрировaниe')
        markup.add(schedule_item, admin_item, group_item)
    else:
        markup.add(schedule_item, group_item)
    return markup