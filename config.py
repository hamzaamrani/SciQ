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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_DEV') or 'sqlite:///' + os.path.join(basedir, 'db/dev.db')
  
class TestingConfig(Config):
    TESTING = os.environ.get('TESTING')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_TEST') or "sqlite:///:memory:"
 
 
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_PROD') or 'sqlite:///' + os.path.join(basedir, 'db/prod.db')
 
 
config = {'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,
          'default': DevelopmentConfig}