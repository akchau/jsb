import unittest
from unittest.mock import patch

from ....http_client import BasicHTTPClient
from ....http_exceptions import (
    BadRequestException,
    ForbiddenException,
    MethodNotAllowedException,
    NonAuthorizedException,
    NotFoundException,
    ServerErrorException,
    UnprocessableEntityException
)


class MockResponseSucess:
    """
    Моковый объект ответа с кодом 200.
    """

    @staticmethod
    def json():
        return {"key": "value"}

    @property
    def status_code(self):
        return 200


class MockResponseNotFound:
    """
    Моковый объект ответа с кодом 404.
    """
    @staticmethod
    def json():
        return {"error": "Not Found"}

    @property
    def status_code(self):
        return 404


class MockResponseBadRequest:
    """
    Моковый объект ответа с кодом 400.
    """
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
    """
    Моковый объект ответа с кодом 500.
    """
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
    """
    Моковый объект ответа с кодом 401.
    """
    @staticmethod
    def json():
        return {"error": "Unauthorized"}

    @property
    def status_code(self):
        return 401


class MockResponseForbiden:
    """
    Моковый объект ответа с кодом 403.
    """
    @staticmethod
    def json():
        return {"error": "Forbiden"}

    @property
    def status_code(self):
        return 403


class MockResponseUnprocessableEntity:
    """
    Моковый объект ответа с кодом 422.
    """
    @staticmethod
    def json():
        return {"error": "Unprocessable entity"}

    @property
    def status_code(self):
        return 422


class MockResponseMethodNotAllowed:
    """
    Моковый объект ответа с кодом 405.
    """
    @staticmethod
    def json():
        return {"error": "Method Not Allowed"}

    @property
    def status_code(self):
        return 405


class TestWithCodes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.host = "api.ru"
        cls.path = 'full/url'
        cls.full_url = f"http://{cls.host}:80/{cls.path}"
        cls.headers_dict = {
            "header_1": "header_value_1",
            "header_2": "header_value_2"
        }
        cls.params_dict = {
            "param_1": "param_value_1",
            "param_2": "param_value_2"
        }
        cls.client = BasicHTTPClient(
            host=cls.host
        )
        cls.client.set_headers(headers=cls.headers_dict)
        cls.client.set_params(params_dict=cls.params_dict)

    def function_call(self):
        return self.client.get(
            path=self.path
        )

    @patch("requests.get", autospec=True)
    def test_with_200(self, mock_get):
        """
        Вызов с ответом 200.
        """
        # Моковый объект ответа
        mock_get.return_value = MockResponseSucess()
        result = self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )
        self.assertEqual(result, MockResponseSucess().json())

    @patch("requests.get", autospec=True)
    def test_with_404(self, mock_get):
        """
        Вызов с ответом 404.
        """
        mock_get.return_value = MockResponseNotFound()
        with self.assertRaises(NotFoundException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_with_400(self, mock_get):
        """
        Вызов с ответом 400.
        """
        mock_get.return_value = MockResponseBadRequest()
        with self.assertRaises(BadRequestException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_with_500(self, mock_get):
        """
        Вызов с ответом 500.
        """
        mock_get.return_value = MockResponseServerError()
        with self.assertRaises(ServerErrorException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_with_401(self, mock_get):
        """
        Вызов с ответом 401.
        """
        mock_get.return_value = MockResponseUnauthorized()
        with self.assertRaises(NonAuthorizedException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_with_403(self, mock_get):
        """
        Вызов с ответом 403.
        """
        mock_get.return_value = MockResponseForbiden()
        with self.assertRaises(ForbiddenException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_with_422(self, mock_get):
        """
        Вызов с ответом 422.
        """
        mock_get.return_value = MockResponseUnprocessableEntity()
        with self.assertRaises(UnprocessableEntityException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_get_with_405(self, mock_get):
        """
        Вызов с ответом 405.
        """
        mock_get.return_value = MockResponseMethodNotAllowed()
        with self.assertRaises(MethodNotAllowedException):
            self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )
