from os import getenv


class Config:
    def setUp(self):
        self.token = getenv('TOKEN')
        self.database_url = getenv('DATABASE_URL')


config = Config()
config.setUp()