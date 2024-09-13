class DbClientException(Exception):
    pass


class ExistException(DbClientException):
    pass


class NotExistException(DbClientException):
    pass
