import os
from pathlib import Path
import typing
import pytz

API_TOKEN = os.getenv('TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
LOGS_BASE_PATH = os.getcwd() + '/' + 'logs'
DB_URI = os.getenv('DB_URI', 'sqlite://bit.sqlite')

DEBUG = False

SKIP_UPDATES = False

LOCAL_TZ = pytz.timezone('Europe/Kiev')

NUMBER_COURSES = 6

TORTOISE_ORM = {
    "connections": {"default": DB_URI},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

LANGUAGES = {'ru': '🇷🇺 Русский', 'en': '🇺🇸 English', 'ua': '🇺🇦 Українська'}
MENU = {'schedule': 'Рacпиcaниe', 'settings': 'Нacтрoйки', 'admin': 'Aдминиcтрирoвaниe'}
SETTIGS = {'notifications': 'Уведомления', 'group-and-subgroups': 'Группа и Подгруппы', 'lang': 'Язык',
           'chat-settings': 'Настройки Чата'}
ADMIN = {'msg-sender': 'Отправить сообщение', 'edit-faculties': 'Редактирование факультетов',
         'edit-groups': 'Редактирование групп', 'edit-subgroups': 'Редактирование подгрупп',
         'edit-events': 'Редактирование событий', 'edit-admins': 'Редактирование админов'}
OPERATIONTS_EVENT = {'edit-title': "Изменить Название", 'edit-date': "Изменить Дату", 'edit-type': "Изменить Тип",
                     'edit-link': 'Изменить Ссылку', 'edit-time': 'Изменить Время', 'delete': 'Удалить'}
TYPE_EVENT = {'test': "Контрольная", 'lecture': 'Лекция', 'exam': 'Экзамен', 'consultation': 'Консультация',
              'practise': 'Практика'}

I18N_DOMAIN = 'bit'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'
LOCALES_DIR = BASE_DIR / 'locales'
