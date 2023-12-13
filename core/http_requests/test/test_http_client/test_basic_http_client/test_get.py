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
    UnprocessableEntityException,
    NotKnownCodeException
)


class MockResponseSucess:
    """
    Моковый объект ответа с кодом 200.
    """

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

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

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

    @staticmethod
    def json():
        return {"error": "Method Not Allowed"}

    @property
    def status_code(self):
        return 405


class MockResponseNotKnownCode:
    """
    Моковый объект ответа с кодом 1000.
    """

    class MockRequest:
        """
        Вложенный моковый объект для Request.
        """
        def __init__(self, method):
            self.method = method

    def __init__(self, method):
        self.request = self.MockRequest(method)

    @staticmethod
    def json():
        return {"key": "value"}

    @property
    def status_code(self):
        return 1000


class TestWithCodes(unittest.TestCase):

    METHOD = "GET"

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

    def function_call(self) -> dict[str, str]:
        """
        Метод делает тестовый вызов метода.

        Returns:
            dict[str, str]: Полезная нагрузка response.
        """
        return self.client.get(
            path=self.path
        )

    @patch("requests.get", autospec=True)
    def test_with_200(self, mock_get):
        """
        Вызов с ответом 200.
        """
        # Моковый объект ответа
        mock_get.return_value = MockResponseSucess(
            method=self.METHOD)
        result: dict[str, str] = self.function_call()
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )
        self.assertEqual(result, mock_get.return_value.json())

    @patch("requests.get", autospec=True)
    def test_with_404(self, mock_get):
        """
        Вызов с ответом 404.
        """
        mock_get.return_value = MockResponseNotFound(
            method=self.METHOD)
        with self.assertRaises(NotFoundException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            f"Такого адресса: \"{self.full_url}\" - не существует!"
        )
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
        mock_get.return_value = MockResponseBadRequest(
            method=self.METHOD)
        with self.assertRaises(BadRequestException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            (f"Неверный запрос на {self.full_url}: "
             f"{mock_get.return_value.content.decode()}\n")
        )
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
        mock_get.return_value = MockResponseServerError(
            method=self.METHOD)
        with self.assertRaises(ServerErrorException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            (f"Ошибка сервера при запросе на {self.full_url}: "
             f"{mock_get.return_value.content.decode()}")
        )
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
        mock_get.return_value = MockResponseUnauthorized(
            method=self.METHOD)
        with self.assertRaises(NonAuthorizedException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            f"Не авторизованны для доступа на \"{self.full_url}\"!"
        )
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
        mock_get.return_value = MockResponseForbiden(
            method=self.METHOD)
        with self.assertRaises(ForbiddenException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            f"Нет доступа на: \"{self.full_url}\"!"
        )
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
        mock_get.return_value = MockResponseUnprocessableEntity(
            method=self.METHOD)
        with self.assertRaises(UnprocessableEntityException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            (f"Неверные данные при запросе на {self.full_url}: "
             f"{mock_get.return_value.json()}")
        )
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
        mock_get.return_value = MockResponseMethodNotAllowed(
            method=self.METHOD)
        with self.assertRaises(MethodNotAllowedException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            f"Метод {self.METHOD} не разрешен для запроса на {self.full_url}."
        )
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )

    @patch("requests.get", autospec=True)
    def test_get_with_not_known_code(self, mock_get):
        """
        Вызов с ответом 405.
        """
        mock_get.return_value = MockResponseNotKnownCode(method=self.METHOD)
        with self.assertRaises(NotKnownCodeException) as context:
            self.function_call()
        self.assertEqual(
            context.exception.args[0],
            (f"Неизвестный код при запросе на {self.full_url}: "
             f"{mock_get.return_value.status_code}.")
        )
        mock_get.assert_called_with(
            url=self.full_url,
            params=self.params_dict,
            headers=self.headers_dict,
        )
