"""
Исключения Api-клиента.
"""
class ApiError(Exception):
    """
    Исключение api-клиента
    """
    def __init__(self, message):
        super().__init__(message)


class ParsingApiResponseError(ApiError):
    """
    Исключение при неудачном парсинге ответа
    """
    def __init__(self, message):
        super().__init__(message)

class InternalApiError(ApiError):
    """
    Исключение при внутренней ошибке при запросе
    """
    def __init__(self, message):
        super().__init__(message)