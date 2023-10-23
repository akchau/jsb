class FileException(Exception):
    """Базовый класс исключений для запросов."""


class NoPathEntity(FileException):
    """Исключение, если передано не значение пути в файл."""
    def __init__(self, message="Переданное значение не является путем файла."):
        super().__init__(message)


class DeleteNotExistFileEntity(FileException):
    """Исключение, если происходит попытка удаления несуществующего файла."""
    def __init__(self, message="Попытка удаления несуществующего файла."):
        super().__init__(message)


class NotSuccessDeleteFileEntity(FileException):
    """Исключение, если после удаления файл все еще существует."""
    def __init__(self, message="Не удалось удалить файл."):
        super().__init__(message)


class OpenedFileDeleteEntity(FileException):
    """Исключение, если после удаления файл все еще существует."""
    def __init__(self, message="Не удалось удалить файл."):
        super().__init__(message)
