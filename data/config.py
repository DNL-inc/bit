import os
import typing

API_TOKEN = os.getenv('TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
LOGS_BASE_PATH = os.getcwd() + '/' + 'logs'
DB_URI = os.getenv('DB_URI', 'sqlite://bit.sqlite')

SKIP_UPDATES = False

LANGUAGES = {'ru': '🇷🇺 Русский', 'en': '🇺🇸 English', 'ua': '🇺🇦 Українська'}
MENU = ['Рacпиcaниe', 'Нacтрoйки', 'Aдминиcтрирoвaниe']


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