import os
from pathlib import Path
import typing

API_TOKEN = os.getenv('TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
LOGS_BASE_PATH = os.getcwd() + '/' + 'logs'
DB_URI = os.getenv('DB_URI', 'sqlite://bit.sqlite')

SKIP_UPDATES = False

LANGUAGES = {'ru': '🇷🇺 Русский', 'en': '🇺🇸 English', '_uk': '🇺🇦 Українська'}
MENU = {'schedule': 'Рacпиcaниe', 'settings': 'Нacтрoйки', 'admin': 'Aдминиcтрирoвaниe'}


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

SETTIGS = {'notifications': 'Уведомления', 'group-and-subgroups': 'Группа и Подгруппы', 'lang': 'Язык', 'chat-settings': 'Настройки Чата'}
ADMIN = {'msg-sender': 'Отправить сообщение', 'edit-faculties': 'Редактирование факультетов', 'edit-groups': 'Редактирование групп', 'edit-subgroups': 'Редактирование подгрупп', 'edit-events': 'Редактирование событий', 'edit-subjects': 'Редактирование предметов', 'edit-admins': 'Редактирование админов'}

I18N_DOMAIN = 'bit'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales' 