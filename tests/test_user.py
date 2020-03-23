from server.database import db
from server.models.models import User
import json

def create_user(username, password):
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return user

def test_add_user(app):
    user_created = create_user("test1", "password1")
    users = User.query.all()
    assert len(users) == 1
    assert users[0].username == "test1"
    assert users[0].password == "password1"


def test_delete_user(app):
    _ = create_user("test1", "password1")
    users = User.query.all()
    assert len(users) == 1
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()  
    users = User.query.all()
    assert len(users) == 0

def test_get_all_user(app):
    _ = create_user("test1", "password1")
    _ = create_user("test2", "password2")
    users = User.query.all()
    assert len(users) == 2

def test_get_user(app):
    _ = create_user("test1", "password1")
    _ = create_user("test2", "password2")
    user = User.query.get(2)
    assert user.username == "test2"
    assert user.password == "password2"