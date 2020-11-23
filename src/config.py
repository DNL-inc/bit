from os import getenv


class Config:
    def setUp(self):
        self.token = getenv('TOKEN')
        self.webhook_host = getenv('WEBHOOK_HOST', '0.0.0.0')
        self.port = getenv('WEBHOOK_PORT', 8443)
        self.webhook_listen = getenv('WEBHOOK_LISTEN', '0.0.0.0')
        self.webhook_url_base = 'https://{}:{}'.format(self.webhook_host, self.port)
        self.webhook_url_path = '/{}/'.format(self.token)
        self.database_url = getenv('DATABASE_URL')


config = Config()
config.setUp()