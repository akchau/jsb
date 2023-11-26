class FileException(Exception):
    """
    Базовый класс исключений для запросов.
    """


class NoPathEntity(FileException):
    """
    Исключение, если передано не значение пути.
    """
    def __init__(self, value: str,
                 message: str = "Переданное значение не является путем - "):
        message = message + f"{value}"
        super().__init__(message)


class DeleteNotExistObjectEntity(FileException):
    """
    Исключение, если происходит попытка удаления несуществующего объекта.
    """
    def __init__(self, path: str,
                 message: str = "Попытка удаления несуществующего объекта - "):
        message = message + path
        super().__init__(message)


class NotSuccessDeleteObjectEntity(FileException):
    """
    Исключение, если после удаления объект все еще существует.
    """
    def __init__(self, path: str,
                 message: str = "Не удалось удалить объект - "):
        message = message + path
        super().__init__(message)


class FileAlreadyExistException(FileException):
    """
    Исключение, если при создании нового файла
    уже существует такой файл.

    Аргументы:

    path (str): Путь файла.
    """
    def __init__(
        self,
        path: str,
        message: str = "Файл {path} уже существует."
    ) -> None:
        formatted_message: str = message.format(path=path)
        super().__init__(formatted_message)


class FileNotYetExistException(FileException):
    """
    Исключение, если при работе с файлом он не существует.

    Аргументы:

    path (str): Путь файла.
    """
    def __init__(
        self,
        path: str,
        message: str = "Файл {path} не существует."
    ) -> None:
        formatted_message: str = message.format(path=path)
        super().__init__(formatted_message)


class NotSucsessCreateFile(FileException):
    """
    Исключение, если при работе с файлом он не существует.

    Аргументы:

    path (str): Путь файла.
    """
    def __init__(
        self,
        path,
        message="Не удалось создать файл {path}."
    ) -> None:
        formatted_message: str = message.format(path=path)
        super().__init__(formatted_message)
