from typing import Any

from .base_exceptions import (
    IsNotBoolException,
    IsNotDictException,
    IsNotIntException,
    IsNotListException,
    IsNotStrException
)


class BaseTypeManager:
    """
    Набор методов для работы с разными типами.
    """
    def validate_list(data: Any) -> list:
        if isinstance(data, list):
            return data
        raise IsNotListException(data=data)

    def validate_dict(data: Any) -> dict:
        if isinstance(data, dict):
            return data
        raise IsNotDictException(data=data)

    def validate_int(data: int | str) -> int:
        """
        Метод валидации целого числа.

        Вернет число, если переданное значение

        - Число

        - Строку, которая содержит цифры

        Args:

            data (int | str):  Валидируемые данные.

        Raises:
            IsNotIntException: Исключение, если тип данных не соответствует.

        Returns:
            int: Возвращаемое целое число
        """
        if isinstance(data, int) or isinstance(data, str) and data.isdigit():
            return int(data)
        raise IsNotIntException(data=data)

    def validate_str(data: Any) -> str:
        if isinstance(data, str) or isinstance(int):
            return str(data).strip()
        raise IsNotStrException(data=data)

    def validate_bool(data: Any) -> bool:
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
