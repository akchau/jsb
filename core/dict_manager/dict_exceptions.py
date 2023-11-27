from typing import Any


class DictException(Exception):
    """
    Базовый класс исключений для работы со словарями.
    """


class IsNotDictException(DictException):
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


class KeyNotExistInDict(DictException):
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


class NotValideTypeForKeyException(DictException):
    """
    Исключение когда передан типа данных, который не может быть ключом словаря.
    """
    def __init__(self, value,
                 message=("Значение {value} имеет тип {type} и"
                          " не может быть ключом словаря.")):
        invalid_type = type(value)
        formatted_message = message.format(value=value, type=invalid_type)
        super().__init__(formatted_message)


class NotValideTypeValueException(DictException):
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