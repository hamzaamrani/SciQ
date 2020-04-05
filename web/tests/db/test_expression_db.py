import unittest
from app import create_app, db
from app.models import Expression, User


expression_template1 = {
            'expression': "x + 2 = 5",
            'solutions': "3",
            'plots': " ",
            'alternate_forms': " ",
            'execution_time': "",
            'symbolic_solutions': "1",
            'results': " ",
            'limits': "",
            'partial_derivates': "",
            'integral': ""
}

expression_template2 = {
            'expression': "x + 2 = 5",
            'solutions': "1",
            'plots': " ",
            'alternate_forms': " ",
            'execution_time': "",
            'symbolic_solutions': "1",
            'results': " ",
            'limits': "",
            'partial_derivates': "",
            'integral': ""
}


class TestExpressionDb(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.db = db
        with self.app.app_context():
            self.db.create_all()


    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_create_expression(self):
        ex = Expression(**expression_template1)
        user = User(username="user1", password="password1", token="token1")
        user.expressions.append(ex)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()
            expressions = Expression.query.all()
        self.assertEqual(len(expressions), 1)
        self.assertEqual(expressions[0].expression, ex.expression)
        self.assertEqual(expressions[0].solutions, ex.solutions)
        self.assertEqual(expressions[0].execution_time, ex.execution_time)

    def test_del_user_cascade(self):
        user = User(username="user1", password="password1", token="token1")
        ex1 = Expression(**expression_template1)
        user.expressions.append(ex1)
        ex2 = Expression(**expression_template2)
        user.expressions.append(ex2)
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

            obj = User.query.filter_by(id=1).one()
            db.session.delete(obj)
            db.session.commit()

            expressions = Expression.query.all()
        self.assertEqual(len(expressions), 0)

        user1 = User(username="user1", password="password1", token="token1")
        ex1 = Expression(**expression_template1)
        user1.expressions.append(ex1)
        ex2 = Expression(**expression_template2)
        user1.expressions.append(ex2)
        user2 = User(username="user2", password="password2", token="token2")
        ex3 = Expression(**expression_template2)
        user2.expressions.append(ex3)
        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            obj = User.query.filter_by(id=1).one()
            db.session.delete(obj)
            db.session.commit()

            expressions = Expression.query.all()
        self.assertEqual(len(expressions), 1)

    def test_del_expression(self):
        user1 = User(username="user1", password="password1", token="token1")
        user2 = User(username="user2", password="password2", token="token2")
        ex1 = Expression(**expression_template1)
        ex2 = Expression(**expression_template2)
        ex3 = Expression(**expression_template2)
        user1.expressions.append(ex1)
        user1.expressions.append(ex2)  
        user2.expressions.append(ex3)
        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()  

            user = User.query.get(1)
            user.expressions.remove(ex2)
            db.session.commit()

            expressions = Expression.query.all()
        self.assertEqual(len(expressions), 2)

    def select_user_expressions(self):
        user1 = User(username="user1", password="password1", token="token1")
        user2 = User(username="user2", password="password2", token="token2")
        ex1 = Expression(**expression_template1)
        ex2 = Expression(**expression_template2)
        ex3 = Expression(**expression_template2)
        user1.expressions.append(ex1)
        user1.expressions.append(ex2)  
        user2.expressions.append(ex3)
        with self.app.app_context():
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()  

            # select expression of user1
            expressions = User.query.get(id=1).expressions

        self.assertEqual(len(expressions), 2)
        self.assertEqual(expression[0], ex1)
        self.assertEqual(expression[1], ex2)

        # select expression of user2 
        with self.app.app_context():
            expressions = User.query.get(id=1).expressions

        self.assertEqual(len(expressions), 1)
        self.assertEqual(expression[0], ex3)

if __name__ == "__main__":
    unittest.main()


