import logging
import os

from flask import Flask
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

heroku = Heroku()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    # app = Flask(__name__)
    app = Flask(__name__, static_url_path="")

    logging.info("In create app; current path is  = " + os.getcwd())

    from web.app.config import config

    app.config.from_object(config[config_name])
    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "/usr/src/sciq/web/app/static/uploads",
    )
    logging.info(
        "Upload folder = "
        + os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "/usr/src/sciq/web/app/static/uploads",
        )
    )

    db.init_app(app)
    if app.config["FLASK_ENV"] == "development":
        with app.app_context():
            db.create_all()
    ma.init_app(app)
    heroku.init_app(app)

    from web.app.models import User, Expression

    migrate.init_app(app, db)

    # Definitions of route API
    from web.app.api import user_api

    app.add_url_rule("/", methods=["GET"], view_func=user_api.index)
    app.add_url_rule("/login", methods=["POST"], view_func=user_api.login)
    app.add_url_rule("/signup", methods=["POST"], view_func=user_api.signup)
    app.add_url_rule(
        "/loggedUser", methods=["GET"], view_func=user_api.loggedUser
    )

    from web.app.api import expression_api

    app.add_url_rule(
        "/submit_expression",
        methods=["POST"],
        view_func=expression_api.submit_expression,
    )
    app.add_url_rule(
        "/sendfile", methods=["POST"], view_func=expression_api.send_file
    )
    app.add_url_rule(
        "/filenames", methods=["GET"], view_func=expression_api.get_filenames
    )

    return app
