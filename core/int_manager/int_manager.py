from .int_exceptoins import IsNotIntException


class IntValidator:

    def __init__(self, data: int) -> None:
        self.data = data

    @property
    def clean_value(self) -> int:
        """
        Проверяет переданные данные и возвращает их,
        если это целое число.

        Raises:
            IsNotIntException: Если переданные данные не целое.

        Returns:
            dict: Валидный словарь.
        """
        if isinstance(self.data, int) and self.data >= 0:
            return self.data
        else:
            raise IsNotIntException(value=self.data)


def validate_int(data: int) -> int:
    """
    Функция вернет валидное положительное число или вызовет ошибку.

    Args:
        data (dict): Словарь.

    Returns:
        dict: Валидный словарь.
    """
    return IntValidator(data=data).clean_value
