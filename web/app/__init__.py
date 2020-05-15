import logging
import os

from flask import Flask, jsonify, render_template, request
from user_agents import parse
#from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from web.app.services.utils.utils import custom_key_func

LIMIT = "1 per day"
limiter = Limiter(key_func=custom_key_func)

# Definitions of route API
from web.app.api import expression_api, user_api
from web.app.api.expression_api import solve_exp
from web.app.api.parser_api import exp2json
from web.app.api.error_handler import reached_limit_requests, login_required
from web.app.config import config
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


#heroku = Heroku()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name):
    app = Flask(__name__, static_url_path="")

    app.config.from_object(config[config_name])

    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "/web/app/static/uploads",
    )
    logging.info(
        "Upload folder = "
        + os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "/web/app/static/uploads",
        )
    )

    from web.app.models import User

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    #heroku.init_app(app)
    jwt.init_app(app)

    migrate.init_app(app, db)

    app.add_url_rule("/", methods=["GET"], view_func=user_api.index)

    app.add_url_rule("/login", methods=["POST"], view_func=user_api.login)

    app.add_url_rule("/logout", methods=["GET"], view_func=user_api.logout)

    app.add_url_rule("/signup", methods=["POST"], view_func=user_api.signup)

    app.add_url_rule("/math", methods=["GET"], view_func=user_api.math)

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

    app.add_url_rule(
        "/applications", methods=["GET"], view_func=user_api.get_applications,
    )

    app.add_url_rule(
        "/applications/add",
        methods=["POST"],
        view_func=user_api.add_application,
    )

    # app.add_url_rule("/filenames",methods=["GET"],view_func=expression_api.get_filenames)

    app.add_url_rule(
        "/api/v1/appid", methods=["GET"], view_func=user_api.get_appid
    )

    app.add_url_rule("/api/v1/parser", methods=["GET"], view_func=exp2json)

    app.add_url_rule("/api/v1/solver", methods=["GET"], view_func=solve_exp)

    app.register_error_handler(429, reached_limit_requests)

    #app.register_error_handler(401, login_required)

    @jwt.unauthorized_loader
    def login_required(error):
        _ = request.stream.read()
        user_agent = parse(request.headers.get("User-Agent"))
        if user_agent.is_pc and "api" not in request.full_path:
            logging.info("handler login required")
            return (
                render_template(
                    "login_required.html",
                ),
                401,
            )
        else:
            return jsonify({"error": "login required"}), 401

    return app
