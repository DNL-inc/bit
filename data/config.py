import os
import typing

API_TOKEN = os.getenv('TOKEN')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
LOGS_BASE_PATH = os.getcwd() + '/' + 'logs'
DB_URI = os.getenv('DB_URI', 'sqlite://bit.sqlite')

SKIP_UPDATES = False