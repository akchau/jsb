import requests

from . import http_exceptions
from ..base_manager.base_manager import BaseTypeManager


class BasicHTTPClient(BaseTypeManager):
    """
    Базовый класс для запроса
    """
    PREFIX = "http"

    def __init__(self, host: str, port: int = "80") -> None:
        self.host = self.slice_path(host)
        self.port = self.validate_int(self.slice_path(port))
        self.domain = f"{self.PREFIX}://{host}:{port}/"
        self._headers = {}
        self._params: dict = {}

    def __get_full_url(self, path: str) -> str:
        """
        Возвращает полный адрес запроса.

        Args:
            path (str): Путь запроса.

        Returns:
            str: Полный адресс запроса.
        """
        clean_path = self.slice_path(value=path)
        return f"{self.domain}{clean_path}"

    def __handle_response(self,
                          response: requests.models.Response) -> dict | None:
        """
        Хендлер обработки ошибок ответа сервера при запросе.

        Выполняется обработка следующих статус кодов.

        Допустимые коды:

        - 200 | 204 |

        Коды ошибок:

        - 400 | 403 | 404 | 405 | 422 |
        """
        match response.status_code:
            case 200:
                return self.parse_response(response.json())
            case 204:
                return None
            case 400:
                raise http_exceptions.BadRequest(
                    reason=response.content.decode("utf-8"),
                    url=response.url
                )
            case 401:
                raise http_exceptions.NonAuthorizedEntity()
            case 403:
                raise http_exceptions.Forbidden(
                    url=response.url_requested
                )
            case 404:
                raise http_exceptions.NotFound(
                    url=response.url_requested
                )
            case 405:
                raise http_exceptions.MethodNotAllowed()
            case 422:
                raise http_exceptions.UnprocessableEntity(
                    data=response.json()
                )
        raise http_exceptions.NotKnownCodeEntity(code=response.status_code)

    def set_params(self, params_dict: dict) -> None:
        """
        Метод добавляет словарь парметров к запросу.

        Args:
            params_dict (dict): Словарь параметров.
        """
        clean_params_dict: dict = self.validate_dict(params_dict)
        for key, value in clean_params_dict.items():
            self._params[self.validate_str(key)] = self.validate_str(value)

    def parse_response(self, data: dict) -> dict:
        """
        Метод обработки ответа.

        Args:
            data (dict): Полезная нагрузка ответа.

        Returns:
            dict: Словарь с распаршеными данными.
        """
        return data

    def set_headers(self, headers: dict) -> None:
        """
        Метод добавляет словарь заголовков к запросу.

        Args:
            headers (dict): Словарь заголовков.
        """
        clean_headers_dict: dict = self.validate_dict(headers)
        for key, value in clean_headers_dict.items():
            self._params[self.validate_str(key)] = self.validate_str(value)

    def get(self, path: str) -> dict | None:
        url: str = self.__get_full_url(path)
        try:
            response: requests.models.Response = requests.get(
                url=url,
                params=self._params,
                headers=self._headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def post(self, path: str, data: dict = None,
             json: dict = None) -> dict | None:
        url: str = self.__get_full_url(path)
        try:
            response: requests.models.Response = requests.post(
                url=url,
                data=data,
                json=json,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def put(self, path: str, data: dict = None,
            json: dict = None) -> dict | None:
        url: str = self.__get_full_url(path)
        try:
            response: requests.models.Response = requests.put(
                url=url,
                data=data,
                json=json,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def delete(self, path: str) -> dict | None:
        url: str = self.__get_full_url(path)
        try:
            response: requests.models.Response = requests.delete(
                url=url,
                params=self._params,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)


class BasicHTTPSClient(BasicHTTPClient):
    PREFIX = "https"


class BaseRequestWithBearerAuthorization(BasicHTTPClient):
    def __init__(self, url, token):
        super().__init__(url)
        self.set_headers({"Authorization": f"Bearer {token}"})
