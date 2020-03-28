from app import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(128),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(128))
    expressions = db.relationship('Expression', cascade="all, delete-orphan" , lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')


class Expression(db.Model):
    __table_args__ = (
        db.UniqueConstraint(
            'user_id',
            'expression',
            name='_user_expression_uc'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False)
    expression = db.Column(db.String(128), index=True, nullable=False)
    expression_type = db.Column(db.String(128), index=True)
    solutions = db.Column(db.String(128))
    #step = db.Column(db.String(128))
    plot = db.Column(db.String(128))
    alternate_forms = db.Column(db.String(128))
    execution_time = db.Column(db.String(128))

    def __repr__(self):
        return '<Expression {} = {}>'.format(self.expression, self.result)

class ExpressionSchema(ma.Schema):
    class Meta:
        fields = (
            'user_id',
            'expression',
            'expression_type',
            'solutions',
            #'step',
            'plot',
            'alternate_forms',
            'execution_time')
