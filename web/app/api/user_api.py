import hashlib
import logging
import secrets

from flask import flash, render_template, request, jsonify, redirect, url_for

from web.app.services.web_services import user_services

global username_global


def index():
    return render_template("index.html", alert=False)


def login():
    global username_global
    try:
        username = request.form["username_login"]
        password = request.form["password_login"]
        md5_password = get_md5(password)
        user_service = user_services.UserService()
        result = user_service.check_credentials(username, md5_password)
        if result:
            username_global = username
            return render_template("loggedUser.html", name=username_global)
        else:
            flash("Username or password are incorrect!")
            return render_template("index.html", alert=True)
    except ValueError as valerr:
        flash(valerr)


def signup():
    try:
        username = request.form["username_signup"]
        password_1 = request.form["password_signup1"]
        password_2 = request.form["password_signup2"]
        if password_1 == password_2:
            password = password_1
            md5_password = get_md5(password)
            user_service = user_services.UserService()
            result = user_service.signup(username, md5_password)
            if result:
                flash("User created! You can login now")
                return render_template("index.html", alert=True)
            else:
                flash("Username already taken!")
                return render_template("index.html", alert=True)
        else:
            # Passwords are not equals
            flash("You have inserted two different password! Please, retry")
            return render_template("index.html", alert=True)
    except ValueError as valerr:
        flash(print(valerr))
        return render_template("index.html")


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
    result = user_services.UserService().get_applications(userid)
    logging.info(request.get_json())
    logging.info(result)
    return render_template("applications.html")


def get_appid():
    return jsonify(success=True, appid=secrets.token_urlsafe(16))


def developer():
    # token = request.args.get("token")
    # decode token and get the username
    user = "belerico"
    return render_template("developer.html", alert=False, name=user)
