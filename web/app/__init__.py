import logging
import os

from flask import Flask
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

heroku = Heroku()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
mongo = PyMongo() 


def create_app(config_name):
    app = Flask(__name__, static_url_path="")

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
    ma.init_app(app)
    heroku.init_app(app)
    mongo.init_app(app)

    from web.app.models import User

    migrate.init_app(app, db)

    # Definitions of route API
    from web.app.api import user_api

    # app.add_url_rule("/prova", 
    #     methods=["POST"], 
    #     view_func=user_api.trova_mongo)

    app.add_url_rule("/", 
        methods=["GET"], 
        view_func=user_api.index)

    app.add_url_rule("/login",
        methods=["POST"],
        view_func=user_api.login)

    app.add_url_rule("/signup",
        methods=["POST"],
        view_func=user_api.signup)

    app.add_url_rule(
        "/loggedUser",
        methods=["GET"],
        view_func=user_api.loggedUser
    )

    from web.app.api import expression_api

    app.add_url_rule(
        "/submit_expression",
        methods=["POST"],
        view_func=expression_api.submit_expression,
    )

    app.add_url_rule(
        "/sendfile",
        methods=["POST"],
        view_func=expression_api.send_file
    )
    
    app.add_url_rule(
        "/filenames",
        methods=["GET"],
        view_func=expression_api.get_filenames
    )

    from web.app.api import collections_api

    app.add_url_rule(
        "/collections",
        methods=["GET"],
        view_func=collections_api.collections
    )

    app.add_url_rule(
        "/save_expression_to_db",
        methods=["POST"],
        view_func=collections_api.save_expression_to_db
    )

    app.add_url_rule(
        "/create_collection",
        methods=["POST"],
        view_func=collections_api.create_collection
    )

    app.add_url_rule(
        "/delete_collection",
        methods=["POST"],
        view_func=collections_api.delete_collection
    )

    return app
