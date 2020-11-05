
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


def course_markup_for_admin():
    markup = types.InlineKeyboardMarkup(row_width=1)
    firstCourse = types.InlineKeyboardButton(text='1-й курс', callback_data="course-1") 
    secondCourse = types.InlineKeyboardButton(text='2-й курс', callback_data="course-2") 
    thirrdCourse = types.InlineKeyboardButton(text='3-й курс', callback_data="course-3") 
    fourthCouse = types.InlineKeyboardButton(text='4-й курс', callback_data="course-4")
    fifthCourse = types.InlineKeyboardButton(text='5-й курс', callback_data="course-5") 
    sixthCourse = types.InlineKeyboardButton(text='6-й курс', callback_data="course-6")
    backButton = types.InlineKeyboardButton(text='Назад', callback_data="backChooseCourse")
    markup.add(firstCourse, secondCourse, thirrdCourse, fourthCouse, fifthCourse, sixthCourse, backButton)
    return markup

def course_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    firstCourse = types.InlineKeyboardButton(text='1-й курс', callback_data="first") 
    secondCourse = types.InlineKeyboardButton(text='2-й курс', callback_data="second") 
    thirrdCourse = types.InlineKeyboardButton(text='3-й курс', callback_data="third") 
    fourthCouse = types.InlineKeyboardButton(text='4-й курс', callback_data="fourth") 
    fifthCourse = types.InlineKeyboardButton(text='5-й курс', callback_data="fifth") 
    sixthCourse = types.InlineKeyboardButton(text='6-й курс', callback_data="sixth")
    markup.add(firstCourse, secondCourse, thirrdCourse, fourthCouse, fifthCourse, sixthCourse)
    return markup

def group_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    group1 = types.InlineKeyboardButton(text='ІПЗ-11', callback_data="ipz11")
    group2 = types.InlineKeyboardButton(text='ІПЗ-12', callback_data="ipz12")
    group3 = types.InlineKeyboardButton(text='ІПЗ-13', callback_data="ipz13")
    backButton = types.InlineKeyboardButton(text='Назад', callback_data="backChooseGroup")
    markup.add(group1, group2, group3, backButton)
    return markup