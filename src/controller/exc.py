"""
Ошибки выбрасываемые контроллером
"""

class ControllerException(Exception):
    """
    Базовое исключение контроллера.
    """

    def __init__(self, message):
        super().__init__(f"Ошибка контроллера: {message}")


class InternalError(ControllerException):
    """
    Внутреняя ошибка сервиса
    """

    def __init__(self, message):
        super().__init__(f"Внутренняя ошибка {message}")
