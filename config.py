"""Flask configuration variables."""
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')

    TESTING = environ.get('TESTING')

    REPOSITORY = environ.get('REPOSITORY')
    SESSION_COOKIE_SECURE = environ.get('SESSION_COOKIE_SECURE') == 'True'
    REMEMBER_COOKIE_SECURE = environ.get('REMEMBER_COOKIE_SECURE') == 'True'

