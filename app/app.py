from typing import List, Dict
from flask import Flask
from flask import request
import hashlib
from flask import abort, redirect, url_for

import json
import services

# TODO: BLUEPRINT FLASK
# TODO: mysql alchemy
app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form["username"]
        password = request.form["password"]

        md5_password = get_md5(password)
        user_service = services.UserService()
        result = user_service.check_credentials(username, md5_password)
        if result:
            return "OK"
        else:
            abort(401)
    except:
        abort(500)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form["username"]
        password = request.form["password"]
        md5_password = get_md5(password)

        user_service = services.UserService()
        result = user_service.signup(username, md5_password)
        if result:
            return "OK"
        else:
            abort(401)

    except:
        abort(500)

def get_md5(password):
    m = hashlib.md5()
    m.update(password.encode())
    md5_password = m.hexdigest()
    return md5_password

@app.route('/')
def index() -> str:
    return "Hello sciq!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
