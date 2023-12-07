import unittest
from unittest.mock import patch

from ....http_client import BasicHTTPClient
from ....http_exceptions import (
    BadRequest,
    Forbidden,
    MethodNotAllowed,
    NonAuthorizedEntity,
    NotFound,
    ServerErrorException,
    UnprocessableEntity
)


class MockResponseSucess:

    @staticmethod
    def json():
        return {"key": "value"}

    @property
    def status_code(self):
        return 200


class MockResponseNotFound:

    @staticmethod
    def json():
        return {"error": "Not Found"}

    @property
    def status_code(self):
        return 404


class MockResponseBadRequest:

    @staticmethod
    def json():
        return {"error": "Bad Request"}

    @property
    def status_code(self):
        return 400

    @property
    def content(self):
        return b"Error BadRequest"


class MockResponseServerError:

    @staticmethod
    def json():
        return {"error": "Server Error"}

    @property
    def status_code(self):
        return 500

    @property
    def content(self):
        return b"Error Serevr Error"


class MockResponseUnauthorized:

    @staticmethod
    def json():
        return {"error": "Unauthorized"}

    @property
    def status_code(self):
        return 401


class MockResponseForbiden:

    @staticmethod
    def json():
        return {"error": "Forbiden"}

    @property
    def status_code(self):
        return 403


class MockResponseUnprocessableEntity:

    @staticmethod
    def json():
        return {"error": "Unprocessable entity"}

    @property
    def status_code(self):
        return 422


class MockResponseMethodNotAllowed:

    @staticmethod
    def json():
        return {"error": "Method Not Allowed"}

    @property
    def status_code(self):
        return 405


class TestWithCode200(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseSucess()
        result = client.get(
            path=self.path
        )
        mock_get.assert_called_with(
            url=f"http://{self.host}:80/{self.path}",
            params=self.params_dict,
            headers=self.headers_dict,
        )
        self.assertEqual(result, {"key": "value"})


class TestWithCode404(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseNotFound()
        with self.assertRaises(NotFound):
            client.get(self.path)


class TestWithCode400(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseBadRequest()
        with self.assertRaises(BadRequest):
            client.get(self.path)


class TestWithCode500(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseServerError()
        with self.assertRaises(ServerErrorException):
            client.get(self.path)


class TestWithCode401(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseUnauthorized()
        with self.assertRaises(NonAuthorizedEntity):
            client.get(self.path)


class TestWithCode403(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseForbiden()
        with self.assertRaises(Forbidden):
            client.get(self.path)


class TestWithCode422(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseUnprocessableEntity()
        with self.assertRaises(UnprocessableEntity):
            client.get(self.path)


class TestWithCode405(unittest.TestCase):

    def setUp(self):
        self.host = "api.ru"
        self.path = 'full/url'
        self.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        self.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }

    @patch("requests.get", autospec=True)
    def test_get(self, mock_get):
        client = BasicHTTPClient(
            host=self.host
        )
        client.set_headers(headers=self.headers_dict)
        client.set_params(params_dict=self.params_dict)
        mock_get.return_value = MockResponseMethodNotAllowed()
        with self.assertRaises(MethodNotAllowed):
            client.get(self.path)
