class ControllerException(Exception):
    pass


class NotAvailable(ControllerException):
    pass


class InternalError(ControllerException):
    pass