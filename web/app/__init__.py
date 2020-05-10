import logging
import os

from flask import Flask, render_template, jsonify, request
from flask_heroku import Heroku
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from user_agents import parse
from flask_jwt_extended import JWTManager

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

LIMIT = "1 per hour"

heroku = Heroku()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[LIMIT]
)
jwt = JWTManager()

def create_app(config_name):
    app = Flask(__name__, static_url_path="")

    from web.app.config import config
    
    app.config.from_object(config[config_name])
    
    app.config["UPLOAD_FOLDER"] = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "/web/app/static/uploads",
    )
    logging.info(
        "Upload folder = "
        + os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "/web/app/static/uploads",
        )
    )
    
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    heroku.init_app(app)
    jwt.init_app(app)

    from web.app.models import User

    migrate.init_app(app, db)

    # Definitions of route API
    from web.app.api import user_api

    app.add_url_rule("/", 
        methods=["GET"], 
        view_func=user_api.index)

    app.add_url_rule("/login",
        methods=["POST"],
        view_func=user_api.login)

    app.add_url_rule("/logout",
        methods=['GET'],
        view_func=user_api.logout)

    app.add_url_rule("/signup",
        methods=["POST"],
        view_func=user_api.signup)

    app.add_url_rule(
        "/math",
        methods=["GET"],
        view_func=user_api.math
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
    
    #app.add_url_rule("/filenames",methods=["GET"],view_func=expression_api.get_filenames)

    @app.errorhandler(429)
    def reached_limit_requests(error):
        user_agent = parse(request.headers.get('User-Agent'))
        if(user_agent.is_pc):
            logging.info("handler limit request")
            return render_template( "math.html", 
                                    alert=True, 
                                    error='Limit reached for a not logged user')
        else:
            return jsonify({'error': 'limit request'}), 429

    return app
