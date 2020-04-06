from app import db,ma
from sqlalchemy import event
from sqlalchemy import *
from sqlalchemy.orm import *

user_expression = db.Table(
    'user_expression', 
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='cascade')),
    db.Column('expression_id', db.Integer, db.ForeignKey('expression.id', ondelete='cascade')),
    db.UniqueConstraint('user_id', 'expression_id'))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(128))
    expressions = db.relationship('Expression', secondary=user_expression, backref="users", lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

@event.listens_for(Session, 'after_flush')
def delete_expression_orphans(session, ctx):
    session.query(Expression).\
        filter(~Expression.users.any()).\
        delete(synchronize_session=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')


class Expression(db.Model):
    __tablename__ = 'expression'

    id = db.Column(db.Integer, primary_key=True)    
    
    expression = db.Column(db.String(128), index=True, nullable=False)
    #expression_type = db.Column(db.String(128), index=True)
    solutions = db.Column(db.String(128), nullable=False)
    plots = db.Column(db.String(128))
    alternate_forms = db.Column(db.String(128))
    execution_time = db.Column(db.String(128))
    symbolic_solutions = db.Column(db.String(128))
    results = db.Column(db.String(128))
    limits = db.Column(db.String(128))
    partial_derivates = db.Column(db.String(128))
    integral = db.Column(db.String(128))

    def __repr__(self):
        return '<Expression {} = {}>'.format(self.expression, self.result)

class ExpressionSchema(ma.Schema):
    class Meta:
        fields = (
            'expression',
            #'expression_type',
            'solutions',
            'plots',
            'alternate_forms',
            'execution_time',
            'symbolic_solutions',
            'results',
            'limits',
            'partial_derivates',
            'integral')
