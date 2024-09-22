class DbClientException(Exception):
    pass


class ModelError(Exception):
    pass


class AuthError(DbClientException):
    """
    Ошибка при аутентификации классов.
    """
    pass


class ExistException(DbClientException):
    """
    Ошибка когда объект существует а не должен.
    """
    pass


class NotExistException(DbClientException):
    """
    Ошибка когда объект не существует а должен.
    """
    pass
