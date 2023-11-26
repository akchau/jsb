from typing import Any

from ..dict_manager.dict_exceptions import (
    IsNotDictException,
    KeyNotExistInDict,
    NotValideTypeForKeyException
)
from ..file_manager.file_exceptions import (
    FileAlreadyExistException,
    FileNotYetExistException,
    NotSucsessCreateFile
    
)


class JsonFileException(Exception):
    """
    Базовый класс исключений для работы с json-файлами.
    """


class NotJsonPathException(JsonFileException):
    """
    Исключение, если передано не значение пути json-файла.

    Аргументы:

    value (str): Значение которое передается в качестве пути.
    """
    def __init__(
        self,
        value: str,
        message: str = "Значение {value} не является путем JSON-файла."
    ) -> None:
        formatted_message: str = message.format(value=value)
        super().__init__(formatted_message)


class EmptyJsonException(JsonFileException):
    """
    Исключение, если json-файл пустой.
    """
    def __init__(
        self,
        path,
        message="Json-файл {path} пустой, невозможно прочитать."
    ):
        formatted_message = message.format(path=path)
        super().__init__(formatted_message)


class NotPermissionForReadException(JsonFileException):
    """
    Исключение, если недостаточно прав на чтение json-файла.
    """
    def __init__(
        self,
        message="Недостаточно прав на чтение json-файла."
    ):
        super().__init__(message)


class AnotherProcessLockFileException(JsonFileException):
    """
    Исключение, если другой процесс заблокировал открытие json-файла.
    """
    def __init__(
        self,
        message="Другой процесс заблокировал работу с json-файлом."
    ):
        super().__init__(message)


class NotPermissionForWriteException(JsonFileException):
    """
    Исключение, если недостаточно прав на запись в json-файл.
    """
    def __init__(
        self,
        message="Недостаточно прав на запись в json-файл."
    ):
        super().__init__(message)


class KeyTupleIsException(JsonFileException):
    """
    Исключение когда передан пустой кортеж ключей.
    """
    def __init__(self, message="Передан пустой кортеж ключей словаря."):
        super().__init__(message)
