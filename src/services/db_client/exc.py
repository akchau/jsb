"""
Модуль с исключениями БД.
"""
class DbClientException(Exception):
    """
    Базовое исклюючение при работе с БД.
    """
    def __init__(self, message):
        super().__init__(message)


class InternalDbError(DbClientException):
    """
    Внутренняя ошибка в БД.
    """
    def __init__(self, message: str):
        super().__init__(f"Внутренняя ошибка сервиса: {message}")


class TransportError(DbClientException):
    """
    Ошибка в транспорте БД.
    """
    def __init__(self, message: str):
        super().__init__(f"Ошибка при парсинге моделей: {message}")


class ModelError(DbClientException):
    """
    Ошибка при парсинге моделей.
    """
    def __init__(self, message: str):
        super().__init__(f"Ошибка при парсинге моделей: {message}")


class ExistException(DbClientException):
    """
    Ошибка когда объект существует а не должен.
    """
    def __init__(self):
        super().__init__("Объект существует. А не должен существовать.")


class NotExistException(DbClientException):
    """
    Ошибка когда объект не существует а должен.
    """
    def __init__(self):
        super().__init__("Объект не существует. А должен существовать.")
