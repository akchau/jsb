class ControllerException(Exception):
    pass


class NotAvailable(ControllerException):
    pass


class InternalError(ControllerException):
    """
    Внутреняя ошибка сервиса
    """
    pass