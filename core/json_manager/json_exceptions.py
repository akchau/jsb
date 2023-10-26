class JsonFileException(Exception):
    """
    Базовый класс исключений для запросов.
    """


class NotJsonPathEntity(JsonFileException):
    """
    Исключение, если передано не значение пути json-файла.
    """
    def __init__(self, value,
                 message="Путь {value} является путем JSON-файла."):
        formatted_message = message.format(value=value)
        super().__init__(formatted_message)


# ?
class OpenedJsonReadEntity(JsonFileException):
    """
    Исключение, если передано не значение пути в файл.
    """
    def __init__(
        self,
        message="Попытка прочитать json-файл открытый в режиме записи."
    ):
        super().__init__(message)


class AlreadyExistEntity(JsonFileException):
    """
    Исключение, если при создании нового json-файла
    уже существует такой файл.
    """
    def __init__(
        self,
        path,
        message="Файл {path} уже существует."
    ):
        formatted_message = message.format(path=path)
        super().__init__(formatted_message)


class NotExistEntity(JsonFileException):
    """
    Исключение, такого json-файла не существует.
    """
    def __init__(
        self,
        path,
        message="Файла {path} не существует."
    ):
        formatted_message = message.format(path=path)
        super().__init__(formatted_message)


class DataIsNotDictEntity(JsonFileException):
    """
    Исключение, если данные загружаемые в json не являются словарем.
    """
    def __init__(
        self,
        path,
        data,
        message="Полученные или загружаемые данные {data} в/из файл {path} имеют тип {data_type} а не слоарь. ."
    ):
        data_type = type(data)
        formatted_message = message.format(
            data=data,
            path=path,
            data_type=data_type
        )
        super().__init__(formatted_message)


class EmptyJsonEntity(JsonFileException):
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


class NotPermissionForReadEntity(JsonFileException):
    """
    Исключение, если недостаточно прав на чтение json-файла.
    """
    def __init__(
        self,
        message="Недостаточно прав на чтение json-файла."
    ):
        super().__init__(message)


class AnotherProcessLockFileEntity(JsonFileException):
    """
    Исключение, если другой процесс заблокировал открытие json-файла.
    """
    def __init__(
        self,
        message="Другой процесс заблокировал работу с json-файлом."
    ):
        super().__init__(message)


class NotPermissionForWriteEntity(JsonFileException):
    """
    Исключение, если недостаточно прав на запись в json-файл.
    """
    def __init__(
        self,
        message="Недостаточно прав на запись в json-файл."
    ):
        super().__init__(message)


class KeyNotExistInJsonDict(JsonFileException):
    """
    Исключение, если при парсинге json-файла произошла
        ошибка - несуществующий ключ.
    """
    def __init__(self, path, key,
                 message="В файле {path} не существует ключа {key}."):
        formatted_message = message.format(path=path, key=key)
        super().__init__(formatted_message)


class NotValideTypeForKey(JsonFileException):
    """
    Исключение когда передан типа данных, который не может быть ключом словаря.

    Args:
        JsonFileException (_type_): _description_
    """
    def __init__(self, value,
                 message=("Значение {value} имеет тип {type} и"
                          " не может быть ключом словаря.")):
        invalid_type = type(value)
        formatted_message = message.format(value=value, type=invalid_type)
        super().__init__(formatted_message)
