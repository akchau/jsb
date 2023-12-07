import requests

from . import http_exceptions
from ..base_manager.base_manager import BaseTypeManager


class BasicHTTPClient(BaseTypeManager):
    """
    Базовый класс для запроса http.

    Использование:

    Методы:

    - set_params - Добавление параметров запроса. Вызывается перед запросом.

    - set_headers - Добавление заголовков запроса. Вызывается перед запросом.

    - parse_response - Обработка ответа.
      Вызывается автоматически после кода 200.

    """
    PREFIX = "http"

    def __init__(self, host: str, port: int = "80") -> None:
        self.host = self.slice_path(host)
        self.port = self.validate_int(self.slice_path(port))
        self.domain = f"{self.PREFIX}://{self.host}:{self.port}/"
        self.headers = {}
        self.params: dict = {}

    def get_full_url(self, path: str) -> str:
        """
        Возвращает полный адрес запроса.

        Args:

            - path (str): Путь запроса.

        Returns:

            - str: Полный адресс запроса.
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

        - 400 | 403 | 404 | 405 | 422 | 401 | 500
        """
        match response.status_code:
            case 200:
                return self.parse_response(response.json())
            case 204:
                return None
            case 400:
                raise http_exceptions.BadRequest(
                    reason=response.content.decode("utf-8"),
                    url=response.url_requested
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
            case 500:
                raise http_exceptions.ServerErrorException(
                    reason=response.content.decode("utf-8")
                )
        raise http_exceptions.NotKnownCodeEntity(code=response.status_code)

    def set_params(self, params_dict: dict) -> None:
        """
        Метод добавляет словарь парметров к запросу.

        Args:

            - params_dict (dict): Словарь параметров.
        """
        clean_params_dict: dict = self.validate_dict(params_dict)
        for key, value in clean_params_dict.items():
            self.params[self.validate_str(key)] = self.validate_str(value)

    def parse_response(self, data: dict) -> dict:
        """
        Метод обработки ответа.

        Args:

            - data (dict): Полезная нагрузка ответа.

        Returns:

            - dict: Словарь с распаршеными данными.
        """
        return data

    def set_headers(self, headers: dict) -> None:
        """
        Метод добавляет словарь заголовков к запросу.

        Args:

            - headers (dict): Словарь заголовков.
        """
        clean_headers_dict: dict = self.validate_dict(headers)
        for key, value in clean_headers_dict.items():
            self.headers[self.validate_str(key)] = self.validate_str(value)

    def get(self, path: str) -> dict | None:
        """
        Метод GET-запроса.

        Args:

            - path (str): Путь запроса.

        Raises:

            - http_exceptions.NotSuccessTryingToConnectEntity: Неудачная
              попытка запроса.

        Returns:

            - dict | None: Словарь с полезными данными ответа.
        """
        url: str = self.get_full_url(path)
        try:
            response: requests.models.Response = requests.get(
                url=url,
                params=self.params,
                headers=self.headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def post(self, path: str, data: dict = None,
             json: dict = None) -> dict | None:
        """
        Метод POST-запроса.

        Args:

            - path (str): Путь запроса.

            - data (dict, optional): Данные запроса.

            - json (dict, optional): json-полезная нагрузка запроса. Defaults to None.

        Raises:

            - http_exceptions.NotSuccessTryingToConnectEntity: Неудачная
              попытка запроса.

        Returns:

            - dict | None: Словарь с полезными данными ответа.
        """
        url: str = self.get_full_url(path)
        try:
            response: requests.models.Response = requests.post(
                url=url,
                data=data,
                json=json,
                headers=self.headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def put(self, path: str, data: dict = None,
            json: dict = None) -> dict | None:
        """
        Метод PUT-запроса.

        Args:

            - path (str): Путь запроса.

            - data (dict, optional): Данные запроса.

            - json (dict, optional): json-полезная нагрузка запроса. Defaults to None.

        Raises:

            - http_exceptions.NotSuccessTryingToConnectEntity: Неудачная
              попытка запроса.

        Returns:
            - dict | None: Словарь с полезными данными ответа.
        """
        url: str = self.get_full_url(path)
        try:
            response: requests.models.Response = requests.put(
                url=url,
                data=data,
                json=json,
                headers=self.headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def delete(self, path: str) -> dict | None:
        """
        Метод DELETE-запроса.

        Args:
            - path (str): Путь запроса.

        Raises:
            - http_exceptions.NotSuccessTryingToConnectEntity: Неудачная
              попытка запроса.

        Returns:
            - dict | None: Словарь с полезными данными ответа.
        """
        url: str = self.get_full_url(path)
        try:
            response: requests.models.Response = requests.delete(
                url=url,
                params=self.params,
                headers=self.headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)


class BasicHTTPSClient(BasicHTTPClient):
    """
    Базовый класс для запроса http.

    Использование:

    Методы:

    - set_params - Добавление параметров запроса. Вызывается перед запросом.

    - set_headers - Добавление заголовков запроса. Вызывается перед запросом.

    - parse_response - Обработка ответа.
      Вызывается автоматически после кода 200.

    """
    PREFIX = "https"


class BasicHTTPlientBearerAuthorization(BasicHTTPClient):
    """
    Базовый класс для запроса http c авторизацией по bearer-токену.

    Использование:

    Методы:

    - set_params - Добавление параметров запроса. Вызывается перед запросом.

    - set_headers - Добавление заголовков запроса. Вызывается перед запросом.

    - parse_response - Обработка ответа.
      Вызывается автоматически после кода 200.

    """
    def __init__(self, host: str, token: str, port: int = "80"):
        super().__init__(host=host, port=port)
        self.set_headers(
            {
                "Authorization": f"Bearer {self.validate_str(token)}"
            }
        )


class BasicHTTPSlientBearerAuthorization(BasicHTTPSClient):
    """
    Базовый класс для запроса https  c авторизацией по bearer-токену.

    Использование:

    Методы:

    - set_params - Добавление параметров запроса. Вызывается перед запросом.

    - set_headers - Добавление заголовков запроса. Вызывается перед запросом.

    - parse_response - Обработка ответа.
      Вызывается автоматически после кода 200.

    """
    def __init__(self, host: str, token: str, port: int = "80"):
        super().__init__(host=host, port=port)
        self.set_headers(
            {
                "Authorization": f"Bearer {self.validate_str(token)}"
            }
        )


class BasicHTTPSlientParamAuthorization(BasicHTTPSClient):
    def __init__(self, host: str, authorization_key: str,
                 token: str, port: int = "80"):
        super().__init__(host=host, port=port)
        self.set_params(
            {
                self.validate_str(authorization_key): self.validate_str(token)
            }
        )
