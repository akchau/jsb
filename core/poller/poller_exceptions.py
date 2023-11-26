class PollingException(Exception):
    """Базовый класс исключений для запросов."""


class TimeOutException(PollingException):
    """Исключение превышено кол-во попыток поллинга."""
    def __init__(self, name,
                 message="Поллинг {name} - превышено количество итераций."):
        formatted_message = message.format(name=name)
        super().__init__(formatted_message)
