import hashlib
import logging
import secrets

from flask import jsonify, make_response, render_template, request

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_optional,
    unset_jwt_cookies,
    jwt_required,
)
from web.app import limiter
from web.app.services.web_services import user_services

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


@jwt_optional
@limiter.exempt
def index():
    if get_jwt_identity() is None:
        return render_template("index.html")
    else:
        return render_template("math.html")


@limiter.exempt
def login():
    try:
        if request.is_json:
            _json = request.json
            username = _json["username"]
            password = _json["password"]

            if username and password:
                md5_password = get_md5(password)
                user_service = user_services.UserService()
                result, id_user = user_service.check_credentials(
                    username, md5_password, id=True
                )
                if result:
                    payload = {"username": username, "id_user": id_user}
                    access_token = create_access_token(identity=payload)

                    resp = make_response(
                        jsonify(
                            {
                                "results": "success",
                                "access_token": access_token,
                            }
                        )
                    )

                    resp.set_cookie(
                        key="access_token_cookie",
                        value=access_token,
                        path="/",
                        httponly=False,
                    )
                    return resp
                else:
                    return jsonify(
                        {"results": "Username or password incorrect!"}
                    )
            else:
                return jsonify({"error": "Missing data!"})
        else:
            return "Request was not JSON", 400
    except ValueError as valerr:
        return jsonify({"error": valerr})


@limiter.exempt
def logout():
    resp = jsonify({"logout": True})
    unset_jwt_cookies(resp)
    return resp, 200


@limiter.exempt
def signup():
    try:
        _json = request.json
        # logging.info("Signup JSON = " + str(_json))
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
                    return jsonify(
                        {"results": "User created! You can login now"}
                    )
                else:
                    return jsonify({"error": "Username already taken!"})
            else:
                # Passwords are not equals
                return jsonify(
                    {
                        "error": "You have inserted two different password! Please, retry"
                    }
                )
        else:
            return jsonify({"error": "One of the field is empty!"})
    except ValueError as valerr:
        return jsonify({"error": valerr})


def get_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    md5_password = m.hexdigest()
    return md5_password


def loggedUser():
    global username_global
    return render_template("loggedUser.html", name=username_global)


@limiter.exempt
@jwt_required
def add_application():
    userid = get_jwt_identity()["id_user"]
    appid = request.get_json()["appid"]
    appname = request.get_json()["appname"]
    result = user_services.UserService().add_application(
        userid, appid, appname
    )
    logging.info(request.get_json())
    logging.info(result)
    return jsonify(
        result=result,
        msg="Application created! You can now use your AppID "
        + appid
        + " to request an API with partial limitations"
        if result
        else "AppID already taken! Refresh the page",
        error=True if not result else False,
    )


@limiter.exempt
@jwt_required
def get_applications():
    userid = get_jwt_identity()["id_user"]
    results = user_services.UserService().get_applications(userid)
    logging.info(request.get_json())
    logging.info(results)
    return render_template("applications.html", results=results)


@limiter.exempt
@jwt_required
def get_appid():
    return jsonify(success=True, appid=secrets.token_urlsafe(16))


@limiter.exempt
@jwt_required
def developer():
    # token = request.args.get("token")
    # decode token and get the username
    user = get_jwt_identity()["username"]
    return render_template("developer.html", alert=False, name=user)


@limiter.exempt
def math():
    return render_template("math.html", alert=False)
