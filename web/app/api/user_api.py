import hashlib
import jwt
from flask import (
    flash,
    render_template,
    request,
    jsonify,
    make_response,
    Response
)
from flask import current_app as app
from flask_jwt_extended import (
    create_access_token, 
    set_access_cookies, 
    jwt_required, 
    unset_jwt_cookies,
    jwt_optional,
    get_jwt_identity
)
from user_agents import parse

import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
import datetime

from web.app.services.web_services import user_services
from web.app import limiter, LIMIT

@jwt_optional
@limiter.exempt
def index():
    if get_jwt_identity() == None:
        return render_template('index.html')
    else:
        return render_template('loggedUser.html')
 
@limiter.exempt
def login():
    try:
        _json = request.json
        username = _json["username"]
        password = _json["password"]

        if username and password:
            md5_password = get_md5(password)
            user_service = user_services.UserService()
            result, id_user = user_service.check_credentials(username, md5_password, id=True)
            if result:
                payload = { 'username': username,
                            'id_user': id_user}
                access_token = create_access_token(identity=payload)

                resp = make_response(jsonify({  'login':True, 
                                                'access_token':access_token}))

                resp.set_cookie(    key='access_token_cookie',
                                    value=access_token,
                                    path='/',
                                    httponly=False)
                return resp

            else:
                return jsonify({'results': "Username or password incorrect!"})
        else:
            return jsonify({"error": "Missing data!"})
    except ValueError as valerr:
        return jsonify({"error": valerr})

@limiter.exempt
def logout():
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200       

@limiter.exempt
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
    return render_template("loggedUser.html", alert=False)
