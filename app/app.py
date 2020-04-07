from typing import List, Dict
from flask import Flask
from flask import request
from flask import Markup
import hashlib
from flask import abort, redirect, url_for, render_template, flash, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename

import os
import json
import services
from prova_costa import Exp, return_object

# TODO: BLUEPRINT FLASK
# TODO: mysql alchemy
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
username_global = None

@app.route('/')
def index():
    return render_template('index.html', alert=False)


@app.route('/login', methods=['POST'])
def login():
    global username_global
    try:
        username = request.form["username_login"]
        password = request.form["password_login"]
        md5_password = get_md5(password)
        user_service = services.UserService()
        result = user_service.check_credentials(username, md5_password)
        if result:
            username_global = username
            return render_template('loggedUser.html', name=username_global)
        else:
            flash("Username or password are incorrect!")
            return render_template('index.html', alert=True)
    except ValueError as valerr:
        flash(valerr)


@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form["username_signup"]
        password_1 = request.form["password_signup1"]
        password_2 = request.form['password_signup2']
        if (password_1 == password_2):
            password = password_1
            md5_password = get_md5(password)
            user_service = services.UserService()
            result = user_service.signup(username, md5_password)
            if result:
                flash("User created! You can login now")
                return render_template('index.html', alert=True)
            else:
                flash("Something went wrong!")
                return render_template('index.html', alert=True)
        else:
            # Passwords are not equals
            flash("You have inserted two different password! Please, retry")
            return render_template('index.html', alert=True)
    except ValueError as valerr:
        flash(print(valerr))
        return render_template('index.html')


def get_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    md5_password = m.hexdigest()
    print("Password = " + password + " and md5 is = " + md5_password)
    return md5_password


@app.route('/submit_expression', methods=['POST'])
def submit_expression():
    global username_global
    expression = request.form["symbolic_expression"]
    # parsed = parser_belo(expression)
    # response_obj = compute_expression(parsed, key[optional], id_equation[optional], dir_plots[optional])
    response_obj = return_object()
    return render_template("show_results.html", alert = False, query = expression, response_obj = response_obj, username = username_global)


@app.route('/loggedUser', methods = ['GET'])
def loggedUser():
    global username_global
    return render_template('loggedUser.html', name=username_global)



#  API - DRAG AND DROP POST FILE TO SERVER
@app.route("/sendfile", methods=["POST"])
def send_file():
    fileob = request.files["file2upload"]
    filename = secure_filename(fileob.filename)
    save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    fileob.save(save_path)
    # open and close to update the access time.
    with open(save_path, "r") as f:
        pass
    flash("File uploaded succesfully!")


# GET NAME OF UPLOADED FILES
@app.route("/filenames", methods=["GET"])
def get_filenames():
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    def modify_time_sort(file_name):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file_name)
        file_stats = os.stat(file_path)
        last_access_time = file_stats.st_atime
        return last_access_time
    filenames = sorted(filenames, key=modify_time_sort)
    return_dict = dict(filenames=filenames)
    return jsonify(return_dict)





if __name__ == '__main__':
    app.secret_key = 'super secret key'  # provide a secret key to run flask server
    app.run(host='0.0.0.0', port='5000', debug=True)
