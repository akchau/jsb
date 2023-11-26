from typing import Any


class IntException(Exception):
    """
    Базовый класс исключений для работы с API-клиентом.
    """


class IsNotIntException(IntException):
    """
    Исключение, если значение не являются целым.

    Аргументы:

    value (Any): Значение которое не является целым
    """
    def __init__(
        self,
        value: Any,
        message: str = "{value} не целое ."
    ) -> None:
        formatted_message: str = message.format(
            value=value,
        )
        super().__init__(formatted_message)
