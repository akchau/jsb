import unittest
from ....http_client import BasicHTTPClient


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.host = "/api.ru/"
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    def test_with_valide_values(self):
        client = BasicHTTPClient(host=self.host)
        client.set_params(
            params_dict=self.params_dict
        )
        self.assertEqual(client.params, self.params_dict)
