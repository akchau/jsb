from typing import Any

from .dict_exceptions import (IsNotDictException,
                              KeyNotExistInDict,
                              NotValideTypeValueException,
                              NotValideTypeForKeyException)


class DictValidator:

    def __init__(self, data: dict) -> None:
        self.data = data

    def get_value_by_key(self, dict_key, data: dict = None):
        if data is None:
            data = self.clean_value
        if not isinstance(dict_key, (int, str, tuple, frozenset)):
            raise NotValideTypeForKeyException(
                value=dict_key
            )
        try:
            return data[dict_key]
        except KeyError:
            raise KeyNotExistInDict(
                    dict_data=data,
                    dict_key=dict_key
                )

    def parse_dict(self, parse_keys: tuple) -> Any:
        result = None
        parsed_dict = self.clean_value.copy()
        for key, data_type in parse_keys:
            parsed_dict = self.get_value_by_key(
                dict_key=key,
                data=parsed_dict
            )
            if str(type(parsed_dict)) == str(data_type):
                result = parsed_dict
            else:
                raise NotValideTypeValueException(
                    value=parsed_dict,
                    expected_type=data_type
                )
        return result

    @property
    def clean_value(self) -> dict:
        """
        Проверяет переданные данные и возвращает их,
        если это словарь.

        Raises:
            IsNotDictException: Если переданные данные не словарь

        Returns:
            dict: Валидный словарь.
        """
        if isinstance(self.data, dict):
            return self.data
        else:
            raise IsNotDictException(data=self.data)


def parse_value_in_dict_by_key(data: dict, dict_key):
    return DictValidator(data=data).get_value_by_key(dict_key=dict_key)


def validate_dict(data: dict) -> dict:
    """
    Функция вернет валидный словарь или вызовет ошибку.

    Args:
        data (dict): Словарь.

    Returns:
        dict: Валидный словарь.
    """
    return DictValidator(data=data).clean_value


def parse_dict(data: dict, parse_keys: tuple[tuple]) -> Any:
    return DictValidator(data=data).parse_dict(parse_keys=parse_keys)
