class JsonFileException(Exception):
    """
    Базовый класс исключений для запросов.
    """


class NotJsonEntity(JsonFileException):
    """
    Исключение, если передано не значение пути в файл.
    """
    def __init__(self, message="Данный файл не является JSON-файлом."):
        super().__init__(message)


class OpenedJsonReadEntity(JsonFileException):
    """
    Исключение, если передано не значение пути в файл.
    """
    def __init__(
        self,
        message="Попытка прочитать json-файл открытый в режиме записи."
    ):
        super().__init__(message)


class AlreadyExistNotJsonEntity(JsonFileException):
    """
    Исключение, если при загрузке
    данных в файл уже существует такой файл.
    """
    def __init__(
        self,
        message="Файл с таким именем уже существует."
    ):
        super().__init__(message)


class DataIsNotDictEntity(JsonFileException):
    """
    Исключение, если данные загружаемые в json не являются словарем.
    """
    def __init__(
        self,
        message="Попытка загрузить не словарь в json-файл."
    ):
        super().__init__(message)


class EmptyJsonEntity(JsonFileException):
    """
    Исключение, если json-файл пустой.
    """
    def __init__(
        self,
        message="Открываемый json-файл пустой."
    ):
        super().__init__(message)


class NotPermissionForReadEntity(JsonFileException):
    """
    Исключение, если json-файл пустой.
    """
    def __init__(
        self,
        message="Открываемый json-файл пустой."
    ):
        super().__init__(message)