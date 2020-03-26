from app import db
from app.models.models import User


def create_user(username, password, token):
    user = User(username=username, password=password, token=token)
    db.session.add(user)
    db.session.commit()
    return user


def test_add_user(app):
    user_created = create_user("test1", "password1", "12345")
    users = User.query.all()
    assert len(users) == 1
    assert users[0].username == "test1"
    assert users[0].password == "password1"


def test_delete_user(app):
    _ = create_user("test1", "password1", "12345")
    users = User.query.all()
    assert len(users) == 1
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    users = User.query.all()
    assert len(users) == 0


def test_get_all_user(app):
    _ = create_user("test1", "password1", "12345")
    _ = create_user("test2", "password2", "12325465")
    users = User.query.all()
    assert len(users) == 2


def test_get_user(app):
    _ = create_user("test1", "password1", "12345")
    _ = create_user("test2", "password2", "12325465")
    user = User.query.get(2)
    assert user.username == "test2"
    assert user.password == "password2"
