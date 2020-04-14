import unittest
from web.app import create_app, db
from web.app.models import User


class TestUserDb(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.db = db
        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def create_user(self, username, password, token):
        user = User(username=username, password=password, token=token)
        with self.app.app_context():
            self.db.session.add(user)
            self.db.session.commit()
        return user

    def test_add_user(self):
        user_created = self.create_user("test1", "password1", "12345")
        with self.app.app_context():
            users = User.query.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].username, "test1")
        self.assertEqual(users[0].password, "password1")

    def test_delete_user(self):
        _ = self.create_user("test1", "password1", "12345")
        with self.app.app_context():
            users = User.query.all()
        self.assertEqual(len(users), 1)
        with self.app.app_context():
            user = User.query.get(1)
        with self.app.app_context():
            self.db.session.delete(user)
            self.db.session.commit()
        with self.app.app_context():
            users = User.query.all()
        self.assertEqual(len(users), 0)

    def test_get_all_user(self):
        _ = self.create_user("test1", "password1", "12345")
        _ = self.create_user("test2", "password2", "12325465")
        with self.app.app_context():
            users = User.query.all()
        self.assertEqual(len(users), 2)

    def test_get_user(self):
        _ = self.create_user("test1", "password1", "12345")
        _ = self.create_user("test2", "password2", "12325465")
        with self.app.app_context():
            user = User.query.get(2)
        self.assertEqual(user.username, "test2")
        self.assertEqual(user.password, "password2")


if __name__ == "__main__":
    unittest.main()
