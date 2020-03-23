from ..database import db
from .. marshmallow import ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

class Expression(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expression = db.Column(db.String(64), index=True, unique=False)
    result = db.Column(db.String(64), index=True, unique=False)
    step = db.Column(db.String(128))

    def __repr__(self):
        return '<Expression {} = {}>'.format(self.username, self.result)

    def __init__(self, user_id, expression, result, step):
        self.user_id = user_id
        self.expression = expression
        self.result = result
        self.step = step

class ExpressionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'expression', 'result', 'step')