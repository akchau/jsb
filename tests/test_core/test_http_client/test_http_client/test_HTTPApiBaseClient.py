import unittest

import settings
from core.http_client.http_client import BasicHTTPClient


class TestAppendPrams(unittest.TestCase):

    RESULT_INT = 0

    def setUp(self) -> None:
        self.test_client = BasicHTTPClient(
            host=settings.UNPACKER_HOST,
            port=settings.UNPACKER_PORT
        )

    def test_with_correct_value(self):
        self.test_client.append_params(key="key", value="value")
        self.assertEqual(self.test_client._params, {"key": "value"})
