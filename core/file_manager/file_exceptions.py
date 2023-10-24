class FileException(Exception):
    """Базовый класс исключений для запросов."""


class NoPathEntity(FileException):
    """Исключение, если передано не значение пути в файл."""
    def __init__(self, value: str,
                 message: str = "Переданное значение не является путем - "):
        message = message + f"{value}"
        super().__init__(message)


class DeleteNotExistObjectEntity(FileException):
    """Исключение, если происходит попытка удаления несуществующего файла."""
    def __init__(self, path: str,
                 message: str = "Попытка удаления несуществующего объекта - "):
        message = message + path
        super().__init__(message)


class NotSuccessDeleteObjectEntity(FileException):
    """Исключение, если после удаления объект все еще существует."""
    def __init__(self, path: str,
                 message: str = "Не удалось удалить объект - "):
        message = message + path
        super().__init__(message)
