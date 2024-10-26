import services.perplexica as px
import unittest
from unittest.mock import patch, MagicMock
from core import create_app

class TestPerplexica(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({
            "TESTING": True
        })

        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("services.perplexica.requests.post")
    def test_query_internet_valid_simple_query(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = { "perplexica_response": "valid query" }
        mock_post.return_value = mock_response

        # query_internet uses requests.post to hit perplexica, so we use a mock
        # method instead with a mock response
        status_code, response_json = px.query_internet("How many legs do ants have?")

        self.assertEqual(status_code, 200, "Should be 200")
        self.assertIsNotNone(response_json, "Response json exists")
        assert response_json is not None
        self.assertGreater(len(response_json.keys()), 0)
