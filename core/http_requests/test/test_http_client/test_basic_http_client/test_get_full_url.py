import unittest
from ....http_client import BasicHTTPClient


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.host = "/api.ru/"
        self.path = '/full/url/'

    def test_with_valide_values(self):
        self.assertEqual(
            BasicHTTPClient(host=self.host).get_full_url(path=self.path),
            "http://api.ru:80/full/url"
        )
