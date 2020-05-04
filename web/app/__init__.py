import logging
import os

from flask import Flask
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Definitions of route API
from web.app.api import expression_api, user_api
from web.app.api.expression_api import solve_exp
from web.app.api.parser_api import exp2json
from web.app.config import config


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

heroku = Heroku()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__, static_url_path="")

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

    from web.app.models import User

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    heroku.init_app(app)

    migrate.init_app(app, db)

    app.add_url_rule("/", methods=["GET"], view_func=user_api.index)

    app.add_url_rule("/login", methods=["POST"], view_func=user_api.login)

    app.add_url_rule("/signup", methods=["POST"], view_func=user_api.signup)

    app.add_url_rule(
        "/loggedUser", methods=["GET"], view_func=user_api.loggedUser
    )

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

    app.add_url_rule(
        "/developer", methods=["GET"], view_func=user_api.developer
    )

    app.add_url_rule("/api/v1/parser", methods=["get"], view_func=exp2json)

    app.add_url_rule("/api/v1/solver", methods=["get"], view_func=solve_exp)

    return app
