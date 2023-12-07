import unittest
from ....http_client import BasicHTTPClient


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.host = "/api.ru/"
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }

    def test_with_valide_values(self):
        client = BasicHTTPClient(host=self.host)
        client.set_headers(
            headers=self.headers_dict
        )
        self.assertEqual(client.headers, self.headers_dict)
