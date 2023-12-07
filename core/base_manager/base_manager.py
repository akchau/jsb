from typing import Any

from .base_exceptions import (
    IndexOutOfListException,
    IsNotBoolException,
    IsNotDictException,
    IsNotIntException,
    IsNotListException,
    IsNotPositiveIntException,
    IsNotStrException,
    KeyNotExistInDict,
    NotKnownTypeOfData,
    NotValideTypeForKeyException
)


class BaseTypeManager:
    """
    Набор методов для работы с разными типами.
    """
    # ПРОТЕСТИРОВАНО
    def validate_list(self, data: Any) -> list:
        """
        Метод валидации списка.

        Вернет список, если переданное значение:

        - Список.

        Args:

            data (list):  Валидируемые данные.

        Raises:
            IsNotListException: Исключение, если тип данных не соответствует.

        Returns:
            list: Возвращаемый список.
        """
        if isinstance(data, list):
            return data
        raise IsNotListException(value=data)

    # ПРОТЕСТИРОВАНО
    def validate_dict(self, data: Any) -> dict:
        if isinstance(data, dict):
            return data
        raise IsNotDictException(data=data)

    # ПРОТЕСТИРОВАНО
    def validate_dict_key(self, data: int | str | tuple | frozenset) -> int | str | tuple | frozenset:
        if not isinstance(data, (int, str, tuple, frozenset)):
            raise NotValideTypeForKeyException(value=data)
        return data

    # ПРОТЕСТИРОВАНО
    def validate_int(self, data: int | str) -> int:
        """
        Метод валидации целого числа.

        Вернет число, если переданное значение:

        - Число.

        - Строку, которая содержит цифры.

        Args:

            data (int | str):  Валидируемые данные.

        Raises:
            IsNotIntException: Исключение, если тип данных не соответствует.

        Returns:
            int: Возвращаемое целое число.
        """
        if isinstance(data, str) and data.isdigit():
            return int(data)
        elif isinstance(data, str) and data[0] == "-":
            int_part = data[1:]
            if int_part.isdigit():
                return int(data)
        elif isinstance(data, int) or isinstance(data, str) and data.isdigit():
            return int(data)
        raise IsNotIntException(value=data)

    # ПРОТЕСТИРОВАНО
    def validate_positive_int(self, data: int | str) -> int:
        """
        Метод валидации целого положительного числа.

        Вернет число, если переданное значение:

        - Положительное число.

        - Строку, которая содержит цифры, а впереди не стоит знак "-".

        Args:

            data (int | str):  Валидируемые данные.

        Raises:
            IsNotIntException: Исключение, если тип данных не соответствует.

        Returns:
            int: Возвращаемое целое положительное число.
        """
        try:
            clean_value = self.validate_int(data=data)
            if clean_value >= 0:
                return clean_value
            raise IsNotPositiveIntException(value=data)
        except IsNotIntException:
            raise IsNotPositiveIntException(value=data)

    def validate_str(self, data: Any) -> str:
        if isinstance(data, str) or isinstance(int):
            return str(data).strip()
        raise IsNotStrException(data=data)

    def validate_bool(self, data: Any) -> bool:
        if isinstance(data, bool):
            return data
        raise IsNotBoolException(data=data)

    def slice_path(self, value: str) -> str:
        """
        Метод который обрезает слеши вначале и в конце.

        Args:
            value (str): Обрезаемое значение.

        Returns:
            str: Чистый путь.
        """
        value: str = self.validate_str(value).strip()
        if value.startswith("/"):
            value = value[1:]
        if value.endswith("/"):
            value = value[:-1]
        return value

    # ПРОТЕСТИРОВАНО
    def get_element_from_list(self, data: list, index: int) -> Any:
        """
        Метод возвращает элемент списка по индексу.

        Args:

            - data (list): Список

            - index (int): Индекс.

        Raises:

            - IndexOutOfListException: Исключение,
              если индекс выходит за границу списка.

        Returns:
            Any: Элемент по индексу.
        """
        clean_index: int = self.validate_positive_int(index)
        max_length: int = len(self.validate_list(data))
        if max_length > clean_index:
            return data[clean_index]
        raise IndexOutOfListException(
            index=clean_index,
            max_length=max_length
        )

    # ПРОТЕСТИРОВАНО
    def get_element_from_dict(self, data: dict,
                              dict_key: int | str | tuple | frozenset) -> Any:
        """
        Метод получает элемент словаря по ключу.

        Args:

            - data (dict): Словарь.

            - dict_key (int | str | tuple | frozenset): Ключ слвоаря.

        Raises:

            - KeyNotExistInDict: Ключ не существует в словаре.

        Returns:

            - Any: Объект по ключу словаря.
        """
        clean_key = self.validate_dict_key(dict_key)
        try:
            return self.validate_dict(data)[clean_key]
        except KeyError:
            raise KeyNotExistInDict(dict_data=data, dict_key=clean_key)

    def parse(self, data: list | dict, keys: list[tuple]) -> Any:
        if isinstance(data, dict):
            result = data.copy()
        elif isinstance(data, list):
            result = [*data]
        else:
            raise NotKnownTypeOfData(value=data, expected_type=[list, dict])
        for current_key, current_type in keys:
            if current_type == dict:
                result = self.get_element_from_dict(data=result, dict_key=current_key)
            elif current_type == list:
                result = self.get_element_from_list(data=result, index=current_key)
        return result
