import os

from core.validators import string_validator


def object_is_file(filepath: str) -> bool:
    """Утилита которая проверяется, является ли объект файлом.

    Args:

        filepath (str): Путь проверяемого файла.

    Returns:
        str: Ответ на вопрос, лежит ли по указанному пути файл.
    """
    if string_validator(value=filepath):
        return os.path.isfile(filepath)
    return False


def delete_file(filepath: str) -> None:
    """
    Args:
        filepath (str): _description_
    """
    if object_is_file(filepath=filepath):
        os.remove(filepath)