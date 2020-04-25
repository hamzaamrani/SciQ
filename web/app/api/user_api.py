import hashlib

from flask import (
    flash,
    render_template,
    request,
    make_response,
    jsonify
)

from web.app.services.web_services import user_services

#global username_global


def index():
    return render_template("index.html", alert=False)


def login():
    #global username_global
    try:
        _json = request.json
        print(_json)
        username = _json["username"]
        password = _json["password"]

        if username and password:
            md5_password = get_md5(password)
            user_service = user_services.UserService()
            result = user_service.check_credentials(username, md5_password)
            if result:
                #return render_template("logged_user.html", name=username_global)
                return jsonify({'results': "Success"},{'username': username})
            else:
                return jsonify({'results': "Username or password incorrect!"})
                #return render_template("index.html", alert=True)
        else:
            return jsonify({"error": "Missing data!"})

    except ValueError as valerr:
        return jsonify({"error": valerr})


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


def logged_user():
    return render_template("logged_user.html")
