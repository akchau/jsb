class RequestException(Exception):
    """
    Базовый класс исключений для запросов.
    """


class BadRequestException(RequestException):
    """
    Исключение для случаев ошибки 400 Bad Request.
    """
    def __init__(self, url: str, reason: str,
                 message="Неверный запрос на {url}: {reason}\n"):
        formatted_message = message.format(
            reason=reason,
            url=url
        )
        super().__init__(formatted_message)


class NonAuthorizedException(RequestException):
    """
    Исключение для случаев ошибки 401 Non Authorized.
    """
    def __init__(self, url: str,
                 message="Не авторизованны для доступа на \"{url}\"!"):
        formatted_message = message.format(url=url)
        super().__init__(formatted_message)


class NotFoundException(RequestException):
    """
    Исключение для случаев ошибки 404 Not Found.
    """
    def __init__(self, url: str,
                 message=("Такого адресса: "
                          "\"{url}\" - не существует!")):
        formatted_message = message.format(url=url)
        super().__init__(formatted_message)


class ForbiddenException(RequestException):
    """
    Исключение для случаев ошибки 403 Not Found.
    """
    def __init__(self, url: str,
                 message="Нет доступа на: \"{url}\"!"):
        formatted_message = message.format(url=url)
        super().__init__(formatted_message)


class MethodNotAllowedException(RequestException):
    """
    Исключение для случаев ошибки 405 Method Not Allowed.
    """
    def __init__(self, url: str, method: str,
                 message="Метод {method} не разрешен для запроса на {url}."):
        formatted_message = message.format(method=method, url=url)
        super().__init__(formatted_message)


class UnprocessableEntityException(RequestException):
    """
    Исключение для случаев ошибки 422 Unprocessable Entity.
    """
    def __init__(self, data, url: str,
                 message="Неверные данные при запросе на {url}: {data}"):
        formatted_message = message.format(data=data, url=url)
        super().__init__(formatted_message)


class ServerErrorException(RequestException):
    """
    Исключение, если внутренняя ошибка сервера.
    """
    def __init__(self, reason: str, url: str,
                 message="Ошибка сервера при запросе на {url}: {reason}"):
        formatted_message = message.format(reason=reason, url=url)
        super().__init__(formatted_message)


class NotKnownCodeException(RequestException):
    """
    Исключение для неизвестного кода ответа.
    """
    def __init__(self, code: int, url: str,
                 message="Неизвестный код при запросе на {url}: {code}."):
        formatted_message = message.format(code=code, url=url)
        super().__init__(formatted_message)


class NotSuccessTryingToConnectException(RequestException):
    """
    Исключение если превышено кол-во попыток подключения.
    """
    def __init__(self, adress,
                 message="Не удалось подключиться по адресу: {adress}."):
        formatted_message = message.format(adress=adress)
        super().__init__(formatted_message)
