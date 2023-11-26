import requests

from . import http_exceptions


class BasicHTTPClient:
    PREFIX = "http"

    def __init__(self, host: str, port: int = "80"):
        self.host = self.__slice(host)
        self.port = self.__slice(port)
        self.domain = f"{self.PREFIX}://{host}:{port}/"
        self._headers = {}
        self._params = {}

    def __get_full_url(self, path):
        clean_path = self.__slice(value=path)
        return f"{self.domain}{clean_path}"

    def __slice(self, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
            if value.startswith("/"):
                value = value[1:]
            if value.endswith("/"):
                value = value[:-1]
            return value
        raise http_exceptions.PathNotString(value=value)

    def __handle_response(self, response):
        """
        Хендлер обработки ошибок ответа сервера при запросе.

        Выполняется обработка следующих статус кодов.

        Допустимые коды:

        - 200

        - 204

        Коды ошибок:

        - 400

        - 404

        - 405

        - 422

        """
        if response.status_code == 200:
            return self.parse_response(response.json())
        elif response.status_code == 204:
            return None
        elif response.status_code == 400:
            raise http_exceptions.BadRequest()
        elif response.status_code == 401:
            raise http_exceptions.NonAuthorizedEntity()
        elif response.status_code == 403:
            raise http_exceptions.Forbidden(url=response.url_requested)
        elif response.status_code == 404:
            raise http_exceptions.NotFound(url=response.url_requested)
        elif response.status_code == 405:
            raise http_exceptions.MethodNotAllowed()
        elif response.status_code == 422:
            raise http_exceptions.UnprocessableEntity(data=response.json())
        else:
            raise http_exceptions.NotKnownCodeEntity(code=response.status_code)

    def append_params(self, key, value):
        self._params[key] = value

    def parse_response(self, data: dict):
        return data

    def set_headers(self, headers: dict):
        self._headers = headers

    def get(self, path: str):
        url = self.__get_full_url(path)
        try:
            response = requests.get(
                url=url,
                params=self._params,
                headers=self._headers
            )
            response.url_requested = url
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def post(self, path: str, data: dict = None, json: dict = None):
        url = self.__get_full_url(path)
        try:
            response = requests.post(
                url=url,
                data=data,
                json=json,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def put(self, path: str, data: dict = None, json: dict = None):
        url = self.__get_full_url(path)
        try:
            response = requests.put(
                url=url,
                data=data,
                json=json,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)

    def delete(self, path: str):
        url = self.__get_full_url(path)
        try:
            response = requests.delete(
                url=url,
                params=self._params,
                headers=self._headers
            )
        except requests.exceptions.ConnectionError:
            raise http_exceptions.NotSuccessTryingToConnectEntity(adress=url)
        return self.__handle_response(response)


class BasicHTTPSClient(BasicHTTPClient):
    PREFIX = "https"


# class BaseRequestWithBearerAuthorization(BasicHTTPClient):
#     def __init__(self, url, token):
#         super().__init__(url)
#         self.set_headers({"Authorization": f"Bearer {token}"})