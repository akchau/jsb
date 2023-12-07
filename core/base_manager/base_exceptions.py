from typing import Any


class BaseTypeException(Exception):
    """
    Базовый класс исключений для работы со словарями.
    """


class IsNotIntException(BaseTypeException):
    """
    Исключение, если значение не являются целым.

    Аргументы:

    value (Any): Значение которое не является целым
    """
    def __init__(
        self,
        value: Any,
        message: str = "{value} не целое число."
    ) -> None:
        formatted_message: str = message.format(
            value=value,
        )
        super().__init__(formatted_message)


class IsNotPositiveIntException(BaseTypeException):
    """
    Исключение, если значение не являются положительным целым.

    Аргументы:

    value (Any): Значение которое не является целым
    """
    def __init__(
        self,
        value: Any,
        message: str = "{value} не целое положительное число."
    ) -> None:
        formatted_message: str = message.format(
            value=value,
        )
        super().__init__(formatted_message)


class IsNotDictException(BaseTypeException):
    """
    Исключение, если данные не являются словарем.

    Аргументы:

    data (Any): Значение которое не является словарем.
    """
    def __init__(
        self,
        data: Any,
        message: str = "{data} - не словарь."
    ) -> None:
        data_type: type = type(data)
        formatted_message: str = message.format(
            data=data,
            data_type=data_type
        )
        super().__init__(formatted_message)


class IsNotListException(BaseTypeException):
    """
    Исключение, если значение не являются списком.

    Аргументы:

    value (Any): Значение которое не является целым
    """
    def __init__(
        self,
        value: Any,
        message: str = "{value} не список ."
    ) -> None:
        formatted_message: str = message.format(
            value=value,
        )
        super().__init__(formatted_message)


class IsNotStrException(BaseTypeException):
    """
    Исключение, если данные не являются словарем.

    Аргументы:

    data (Any): Значение которое не является словарем.
    """
    def __init__(
        self,
        data: Any,
        message: str = "{data}\n--\nне слоарь. ."
    ) -> None:
        data_type: type = type(data)
        formatted_message: str = message.format(
            data=data,
            data_type=data_type
        )
        super().__init__(formatted_message)


class IsNotBoolException(BaseTypeException):
    """
    Исключение, если данные не являются словарем.

    Аргументы:

    data (Any): Значение которое не является словарем.
    """
    def __init__(
        self,
        data: Any,
        message: str = "{data}\n--\nне слоарь. ."
    ) -> None:
        data_type: type = type(data)
        formatted_message: str = message.format(
            data=data,
            data_type=data_type
        )
        super().__init__(formatted_message)


class KeyNotExistInDict(BaseTypeException):
    """
    Исключение, если такого ключа нет в словаре.

    Аргументы:

    key (Any): Значение которое не является словарем.
    """
    def __init__(
        self,
        dict_key,
        dict_data: Any,
        message: str = "Ключа {dict_key} нет в словаре\n{dict_data}."
    ) -> None:
        formatted_message: str = message.format(
            dict_key=dict_key,
            dict_data=dict_data
        )
        super().__init__(formatted_message)


class NotValideTypeForKeyException(BaseTypeException):
    """
    Исключение когда передан типа данных, который не может быть ключом словаря.
    """
    def __init__(self, value,
                 message=("Значение {value} имеет тип {type} и"
                          " не может быть ключом словаря.")):
        invalid_type = type(value)
        formatted_message = message.format(value=value, type=invalid_type)
        super().__init__(formatted_message)


class NotValideTypeValueException(BaseTypeException):
    """
    Исключение когда при парсинге словаря получен неверный тип данных.
    """
    def __init__(
        self,
        value: Any,
        expected_type: type,
        message: str = ("Значение {value} имеет тип {type} а"
                        " не ожидаемый тип {expected_type}.")) -> None:
        invalid_type = type(value)
        formatted_message = message.format(
            value=value,
            type=invalid_type,
            expected_type=expected_type
        )
        super().__init__(formatted_message)


class NotKnownTypeOfData(BaseException):
    """
    Исключение когда при парсинге словаря получен необрабатываемый тип данных.
    """
    def __init__(
        self,
        value: Any,
        expected_type: list,
        message: str = ("Значение {value} имеет тип {type} а"
                        " не один из ожидаемых типов {expected_type}.")) -> None:
        invalid_type = type(value)
        formatted_message = message.format(
            value=value,
            type=invalid_type,
            expected_type=expected_type
        )
        super().__init__(formatted_message)


class IndexOutOfListException(BaseException):
    """
    Исключение при выходе за границы массива.
    """
    def __init__(
        self,
        index: int,
        max_length: int,
        message: str = ("Значение {index} вышло за границы массива, "
                        "который имеет длинну {max_length}")) -> None:
        formatted_message = message.format(
            index=index,
            max_length=max_length
        )
        super().__init__(formatted_message)