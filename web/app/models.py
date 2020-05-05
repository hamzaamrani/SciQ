from web.app import db, ma

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(128), index=True, unique=True, nullable=False
    )
    password = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("username", "password")
