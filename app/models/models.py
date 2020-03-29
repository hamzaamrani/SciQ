from app import db, ma


user_expression = db.Table('user_expression', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('expression_id', db.Integer, db.ForeignKey('expression.id')),
    db.PrimaryKeyConstraint('user_id', 'expression_id'))


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
    expressions = db.relationship('Expression', secondary=user_expression, backref="user", cascade="all, delete-orphan" , lazy='dynamic', single_parent=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')


class Expression(db.Model):
    __tablename__ = 'expression'

    id = db.Column(db.Integer, primary_key=True)    
    
    expression = db.Column(db.String(128), index=True, nullable=False)
    expression_type = db.Column(db.String(128), index=True)
    solutions = db.Column(db.String(128), nullable=False)
    plot = db.Column(db.String(128))
    alternate_forms = db.Column(db.String(128))
    execution_time = db.Column(db.String(128))

    def __repr__(self):
        return '<Expression {} = {}>'.format(self.expression, self.result)

class ExpressionSchema(ma.Schema):
    class Meta:
        fields = (
            'expression',
            'expression_type',
            'solutions',
            'plot',
            'alternate_forms',
            'execution_time')
