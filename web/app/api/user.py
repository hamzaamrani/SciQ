from app import db
from . import user_blueprint
from flask import request, jsonify, send_from_directory
from app.models import User, UserSchema, Expression, ExpressionSchema
import os

base_folder_image = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'plot')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
expression_schema = ExpressionSchema()
expressions_schema = ExpressionSchema(many=True)

@user_blueprint.route('/index', methods=['GET'])
def home():
    return "ciao figlio di una buona donna"
    
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


@user_blueprint.route('/<username>/expression', methods=['GET'])
def get_ex_for_user(username):
    expressions = Expression.query.filter(Expression.user.any(username=username)).all()
    return jsonify(expressions_schema.dump(expressions))



@user_blueprint.route('/plot/<filename>', methods=['GET'])
def get_plot(filename):
        return send_from_directory(directory=base_folder_image, filename=filename)

@user_blueprint.route('/plot', methods=['POST'])
def save_plot():
    # in teoria bisognerebbe controllare che non ci siano più plot,
    # nel caso salvare ogni plot in modo distinto
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        #filename = secure_filename(file.filename)
        file.save(os.path.join(base_folder_image, file.filename))
        return "immagine {} salvata correttamente".format(file.filename)