import os

#export MY_VAR="123"

class Environment:
    DEV = 'dev'
    PROD = 'prod'

    URL = {
        DEV: 'https://playground.learnqa.ru/api_dev',
        PROD: 'https://playground.learnqa.ru/api'
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URL:
            return self.URL[self.env]
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}")

ENV_OBJECT = Environment()