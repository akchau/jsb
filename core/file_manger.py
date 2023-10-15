import os
from typing import Union


def object_is_file(filepath: str) -> bool:
    """
    Утилита которая проверяется, является ли объект файлом.

    Args:

        filepath (str): Путь проверяемого файла.

    Returns:

        str: Ответ на вопрос, лежит ли по указанному пути файл.
    """
    if isinstance(filepath, str):
        return os.path.isfile(filepath)
    return False


def delete_file(filepath: str) -> Union[str, None]:
    """
    Утилита которая удаляет файл.

    Args:

        - filepath (str): Путь удаялемого файла.
    Returns:

        - Union[str, None]: Если файл удален - путь файла, или None.
    """
    if object_is_file(filepath=filepath):
        try:
            os.remove(filepath)
        except PermissionError:
            return None
    else:
        return None
    if not object_is_file(filepath=filepath):
        return filepath
    return None
