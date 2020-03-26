from app import db
from . import user_blueprint
from flask import request, jsonify
from app.models.models import User, UserSchema

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_blueprint.route('/home', methods=['GET'])
def home():
    return "HOME PAGE"

# create user
@user_blueprint.route('/', methods=['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']
    token = request.json['token']
    user = User(username=username, password=password, token=token)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)

# get all users
@user_blueprint.route('/', methods=['GET'])
def get_all_user():
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify(result)

# get a user
@user_blueprint.route('/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(int(id))
    return user_schema.jsonify(user)

# delete a user
@user_blueprint.route('/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(int(id))
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)