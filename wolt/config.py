import os
import environ


env = environ.Env()


class BaseConfig(object):

    PROJECT = "wolt"

    DEBUG = env.bool("FLASK_DEBUG", True)
    TESTING = False

    LOG_FOLDER = os.path.join(os.path.join("/var/log", "wolt"))


class TestConfig(BaseConfig):
    TESTING = True
