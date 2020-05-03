import hashlib
import jwt
from flask import (
    flash,
    render_template,
    request,
    jsonify
)
import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
import datetime

from web.app.services.web_services import user_services
from web.app.services.utils.limit_request import get_user_type
from web.app import limiter, LIMIT
from flask import current_app as app

def index():
    return render_template("index.html", alert=False)
    
def login():
    try:
        _json = request.json
        #logging.info("Login JSON = " + str(_json))
        username = _json["username"]
        password = _json["password"]

        if username and password:
            md5_password = get_md5(password)
            user_service = user_services.UserService()
            result = user_service.check_credentials(username, md5_password)
            if result:
                payload = {
                    "sub": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=4),
                }
                access_token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS512').decode("utf-8")
                logging.info("Token {} create con username {}".format(access_token, username))
                return jsonify({"results": "Success", 
                                "username": username,
                                "access_token": access_token})
            else:
                return jsonify({'results': "Username or password incorrect!"})
        else:
            return jsonify({"error": "Missing data!"})
    except ValueError as valerr:
        return jsonify({"error": valerr})



def signup():
    try:
        _json = request.json
        #logging.info("Signup JSON = " + str(_json))
        username = _json["username"]
        password_1 = _json["password1"]
        password_2 = _json["password2"]

        if username and password_1 and password_2:
            if password_1 == password_2:
                password = password_1
                md5_password = get_md5(password)
                user_service = user_services.UserService()
                result = user_service.signup(username, md5_password)
                if result:
                    return jsonify({"results" : "User created! You can login now"})
                else:
                    return jsonify({"error" : "Username already taken!"})
            else:
                # Passwords are not equals
                return jsonify({"error" : "You have inserted two different password! Please, retry"})
        else:
            return jsonify({"error" : "One of the field is empty!" })
    except ValueError as valerr:
        return jsonify({"error" : valerr})



def get_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    md5_password = m.hexdigest()
    return md5_password

@limiter.exempt
def loggedUser():
    return render_template("loggedUser.html", alert_limit=False)
