import unittest
from waAPI import NoAPIKeyException, waAPI, ExpressionException, Expression


KEY = 'V2WJ46-EEXEV95WXG'


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_key(self):
        with self.assertRaises(NoAPIKeyException):
            waAPI(None)

    def test_valid_full_results(self):
        client_api = waAPI(KEY)
        self.assertEqual(client_api.full_results(query=None),
                         'Sorry, I did not get your question.')

    def test_valid_expression_query(self):
        query = 'x^3 - y^2 = 23'
        api = waAPI(KEY)
        results = api.full_results(query=query)
        with self.assertRaises(ExpressionException):
            Expression(query=None, results=results)

    def test_valid_expression_results(self):
        query = 'x^3 - y^2 = 23'
        with self.assertRaises(ExpressionException):
            Expression(query=query, results=None)

    def test_valid_expression_success_true(self):
        query = 'x^3 - y^2 = 23'
        api = waAPI(KEY)
        results = api.full_results(query=query)
        exp = Expression(query=query, results=results)
        self.assertTrue(exp.success)

    def test_valid_expression_success_false(self):
        query = 'x^3( - y^2 = 23'
        api = waAPI(KEY)
        results = api.full_results(query=query)
        exp = Expression(query=query, results=results)
        self.assertFalse(exp.success)


if __name__ == '__main__':
    unittest.main()
