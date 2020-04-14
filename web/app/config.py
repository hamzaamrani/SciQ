import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = os.environ.get('FLASK_ENV')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEV')
    FLASK_ENV = 'development'


class TestingConfig(Config):
    TESTING = os.environ.get('TESTING')
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_PROD')
    FLASK_ENV = 'production'
    FLASK_APP = 'run_prod.py'


config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}
          
DB_CONFIG_DEV = {
    'user': 'root',
    'password': 'root',
    'host': 'db',
    'port': '3306',
    'database': 'sciq'
}

DB_CONFIG_PROD = {
    'user': 'bc723c98218203',
    'password': 'e9caa73c',
    'host': 'eu-cdbr-west-02.cleardb.net',
    'port': '3306',
    'database': 'heroku_62e37664534fe76'
}
