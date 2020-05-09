import unittest
from unittest.mock import patch, Mock
from flask_jwt_extended import create_access_token

from web.app import create_app


class TestLimiRequest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    @patch('web.app.api.expression_api.compute_expression')
    @patch('web.app.api.expression_api.render_template')
    @patch('web.app.api.expression_api.parse_2_latex')
    def test_limit(self, mock_parse_2_latex, mock_compute_expression, mock_render_template):
        mock_parse_2_latex.return_value = " "
        mock_compute_expression.return_value = " "
        mock_render_template.return_value = " "
        response = self.client.post(    '/submit_expression', 
                                        headers={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
                                        data='symbolic_expression=' + "2 + 2 = 0",
                                        content_type='application/x-www-form-urlencoded'
                                    )
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(    '/submit_expression', 
                                        headers={'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
                                        data='symbolic_expression=' + "2 + 2 = 0",
                                        content_type='application/x-www-form-urlencoded'
                                    )
        self.assertEqual(response.status_code, 429)

        self.assertEqual(mock_compute_expression.call_count, 1)
        self.assertEqual(mock_render_template.call_count, 1)
        self.assertEqual(mock_parse_2_latex.call_count, 1)

    
    @patch('web.app.api.expression_api.compute_expression')
    @patch('web.app.api.expression_api.render_template')
    @patch('web.app.api.expression_api.parse_2_latex')
    def test_no_limit(self, mock_parse_2_latex, mock_compute_expression, mock_render_template):
        with self.app.app_context():
            access_token = create_access_token(identity={'username': 'prova', 'id_user': 1})
        mock_parse_2_latex.return_value = " "
        mock_compute_expression.return_value = " "
        mock_render_template.return_value = " "
        self.client.set_cookie('localhost','access_token_cookie', str(access_token))
        response = self.client.post(    '/submit_expression', 
                                        headers={   'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
                                        data='symbolic_expression=' + "2 + 2 = 0",
                                        content_type='application/x-www-form-urlencoded'
        )
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post(    '/submit_expression', 
                                        headers={   'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
                                        data='symbolic_expression=' + "2 + 2 = 0",
                                        content_type='application/x-www-form-urlencoded'
        )   
        self.assertEqual(response.status_code, 200)

        response = self.client.post(    '/submit_expression', 
                                        headers={   'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'},
                                        data='symbolic_expression=' + "2 + 2 = 0",
                                        content_type='application/x-www-form-urlencoded'
        )   
        self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_compute_expression.call_count, 3)
        self.assertEqual(mock_render_template.call_count, 3)
        self.assertEqual(mock_parse_2_latex.call_count, 3)
              

if __name__ == "__main__":
    unittest.main()
