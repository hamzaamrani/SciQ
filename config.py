import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #TESTING = environ.get('TESTING')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    DEBUG = os.environ.get('DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEV') or 'sqlite:///' + os.path.join(basedir, 'db/db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

class ConfigTest(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_TEST') or 'sqlite:///' + os.path.join(basedir, 'db/test.sqlite')