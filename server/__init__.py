from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .database import db
    db.init_app(app)

    from .cli import cli_init_app
    cli_init_app(app)
    
    from .migrate import migrate
    migrate.init_app(app,db)

    from .marshmallow import ma
    ma.init_app(app)

    from .api import user_blueprint, expression_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(expression_blueprint)

    return app

