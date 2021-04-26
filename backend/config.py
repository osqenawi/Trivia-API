"""Flask configuration."""
from os import environ
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config:
    """Base config."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_SQLALCHEMY_DATABASE_URI')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = environ.get('TESTING_SQLALCHEMY_DATABASE_URI')
    DEBUG = False
    TESTING = True

