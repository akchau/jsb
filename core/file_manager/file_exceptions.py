from typing import Any


class FileException(Exception):
    """
    Базовый класс исключений для запросов.
    """


class NotTxtPathException(FileException):
    """
    Исключение, если передано не значение пути txt-файла.

    Аргументы:

    value (str): Значение которое передается в качестве пути.
    """
    def __init__(
        self,
        value: str,
        message: str = "Значение {value} не является путем txt-файла."
    ) -> None:
        formatted_message: str = message.format(value=value)
        super().__init__(formatted_message)


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
        path: str,
        message: str = "Не удалось создать файл {path}."
    ) -> None:
        formatted_message: str = message.format(path=path)
        super().__init__(formatted_message)


class NotSucsessWriteDataToFile(FileException):
    """
    Исключение, если не удалось записать данные в файл.

    Аргументы:

    - path (str): Путь файла.

    - data (Any): Данные которые не удалось записать в файл.

    """
    def __init__(
        self,
        path: str,
        data: Any,
        message="Не удалось записать данные {data} в файл {path}."
    ) -> None:
        formatted_message: str = message.format(
            data=data,
            path=path
        )
        super().__init__(formatted_message)
