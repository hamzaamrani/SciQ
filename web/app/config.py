import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DEBUG = os.environ.get("DEBUG")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configuration for manage token in cookie and json body
    JWT_TOKEN_LOCATION = ['cookies', 'json']
    JWT_ACCESS_TOKEN_EXPIRES = False
    JWT_IDENTITY_CLAIM = 'identity'
    JWT_USER_CLAIMS = 'user_claims'
    JWT_ERROR_MESSAGE_KEY = 'error'

    # configuration for cookie
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_ACCESS_COOKIE_PATH = '/' # TODO modify
    JWT_REFRESH_COOKIE_PATH = '/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SECURE = False
    JWT_SESSION_COOKIE = True

    # configuration for json
    JWT_JSON_KEY = 'access_token'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_DEV")
    MONGO_URI = os.environ.get("MONGO_URI")
    FLASK_ENV = "development"



class TestingConfig(Config):
    TESTING = os.environ.get("TESTING")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    MONGO_URI = os.environ.get("MONGO_URI")
    FLASK_ENV = "development"



class PreProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_PRE_PROD")
    MONGO_URI = os.environ.get("MONGO_URI_PRE_PROD")
    FLASK_ENV = "production"
    FLASK_APP = "run_prod.py"
    

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI_PROD")
    MONGO_URI = os.environ.get("MONGO_URI_PROD")
    FLASK_ENV = "production"
    FLASK_APP = "run_prod.py"



config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
    "pre_prod" : PreProductionConfig,
}

DB_CONFIG_DEV = {
    "user": "root",
    "password": "root",
    "host": "db",
    "port": "3306",
    "database": "sciq",
}

DB_CONFIG_PROD = {
    "user": "bc723c98218203",
    "password": "e9caa73c",
    "host": "eu-cdbr-west-02.cleardb.net",
    "port": "3306",
    "database": "heroku_62e37664534fe76",
}

OCR_CONFIG = {
    'model_dir': "./data/ocr/",
    'drive_id': '1pK9mMjQpkwxeoievIM2Vzoo8NDvTZZdW'
}

DB_CONFIG_PRE_PROD = {
    "user": "bdd2e662bdbe1b",
    "password": "2e134689",
    "host": "eu-cdbr-west-03.cleardb.net",
    "port": "3306",
    "database": "heroku_8c7f90193d110bd",
}
