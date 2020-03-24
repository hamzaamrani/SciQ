from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from .api import user_blueprint, expression_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(expression_blueprint)

    from .models.models import User, Expression

    return app

