from web.app import db


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


class Applications(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    appid = db.Column(db.String(128), index=True, unique=True, nullable=False)
    name = db.Column(db.String(128), index=True, unique=False, nullable=False)
    username_fk = db.Column(db.Integer, db.ForeignKey("user.id"), index=True)
