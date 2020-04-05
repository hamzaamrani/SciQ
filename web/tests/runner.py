import unittest
from .db.test_user_db import TestUserDb
from .db.test_expression_db import TestExpressionDb

def suite():
    suite = unittest.TestSuite()
    suite.addTests(TestUserDb)
    suite.addTests(TestExpressionDb)
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
