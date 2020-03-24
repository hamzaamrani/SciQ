from server import db
from . import user_blueprint
from .decorators import decorator
from flask import request, jsonify
from server.models.models import User, UserSchema
import os

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# create user
@user_blueprint.route('/user', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    token = request.json['token']
    user = User(username=username, password=password, token=token)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

# get all users
@user_blueprint.route('/user', methods=['GET'])
def get_all_user():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

# get a user
@user_blueprint.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

# delete a user
@user_blueprint.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)