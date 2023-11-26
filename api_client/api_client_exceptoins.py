from core.int_manager.int_exceptoins import IsNotIntException


class ApiClientException(Exception):
    """
    Базовый класс исключений для работы с API-клиентом.
    """


class NotSuccsessRefreshNumberOfTrying(ApiClientException):
    """
    Исключение, если попытка обновления количества оставшихся попыток неудачна.
    """
    def __init__(
        self,
        message: str = "Попытка перезапси количества попыток неудачна!."
    ) -> None:
        super().__init__(message)
