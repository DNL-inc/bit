
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


def course_markup(callback_for_back='backChooseCourse', admin=''):
    markup = types.InlineKeyboardMarkup(row_width=1)
    firstCourse = types.InlineKeyboardButton(text='1-й курс', callback_data=admin+"-"+"course-1") 
    secondCourse = types.InlineKeyboardButton(text='2-й курс', callback_data=admin+"-"+"course-2") 
    thirrdCourse = types.InlineKeyboardButton(text='3-й курс', callback_data=admin+"-"+"course-3") 
    fourthCouse = types.InlineKeyboardButton(text='4-й курс', callback_data=admin+"-"+"course-4") 
    fifthCourse = types.InlineKeyboardButton(text='5-й курс', callback_data=admin+"-"+"course-5") 
    sixthCourse = types.InlineKeyboardButton(text='6-й курс', callback_data=admin+"-"+"course-6")
    markup.add(firstCourse, secondCourse, thirrdCourse, fourthCouse, fifthCourse, sixthCourse)
    if  callback_for_back != '':
        backButton = types.InlineKeyboardButton(text='Назад', callback_data=callback_for_back)
        markup.add(backButton)
    return markup

def schedule_markup(caption="", back=""):
    markup = types.InlineKeyboardMarkup(row_width=1)
    monday = types.InlineKeyboardButton(
        text='Понеділок', callback_data=caption+"-"+"schedule_monday")
    tuesday = types.InlineKeyboardButton(
        text='Вівторок', callback_data=caption+"-"+"schedule_tuesday")
    wednesday = types.InlineKeyboardButton(
        text='Середа', callback_data=caption+"-"+"schedule_wednesday")
    thursday = types.InlineKeyboardButton(
        text='Четвер', callback_data=caption+"-"+"schedule_thursday")
    friday = types.InlineKeyboardButton(
        text='П\'ятниця', callback_data=caption+"-"+"schedule_friday")
    saturday = types.InlineKeyboardButton(text='Субота', callback_data=caption+"-"+"schedule_saturday")
    sunday = types.InlineKeyboardButton(text='Неділя', callback_data=caption+"-"+"schedule_sunday")
    markup.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    if back != "":
        markup.add(types.InlineKeyboardButton(text='Назад', callback_data=back))
    return markup