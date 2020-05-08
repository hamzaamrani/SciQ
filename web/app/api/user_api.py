import hashlib
import logging
import secrets

from flask import jsonify, render_template, request

from web.app.services.web_services import user_services

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


def index():
    return render_template("index.html", alert=False)


def login():
    try:
        if request.is_json:
            logging.info("Request.data = " + str(request.data))
            _json = request.get_json()
            logging.info("Login JSON = " + str(_json))
            username = _json["username"]
            password = _json["password"]
            if username and password:
                md5_password = get_md5(password)
                user_service = user_services.UserService()
                result = user_service.check_credentials(username, md5_password)
                if result:
                    return jsonify(
                        {"results": "Success", "username": username}
                    )
                else:
                    return jsonify(
                        {"results": "Username or password incorrect!"}
                    )
            else:
                return jsonify({"error": "Missing data!"})
        else:
            return "Request was not JSON", 400
    except ValueError as valerr:
        logging.info("Errore porco schifo, err = " + str(valerr))


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


def add_application():
    userid = request.get_json()["userid"]
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
        + " to request an API without limitations"
        if result
        else "AppID already taken! Refresh the page",
        error=True if not result else False,
    )


def get_applications():
    userid = request.args.get("userid")
    results = user_services.UserService().get_applications(userid)
    logging.info(request.get_json())
    logging.info(results)
    return render_template("applications.html", results=results)


def get_appid():
    return jsonify(success=True, appid=secrets.token_urlsafe(16))


def developer():
    # token = request.args.get("token")
    # decode token and get the username
    user = "belerico"
    return render_template("developer.html", alert=False, name=user)


def math():
    return render_template("math.html")
