import os


def object_is_file(filepath: str) -> bool:
    """Утилита которая проверяется, является ли объект файлом.

    Args:

        filepath (str): Путь проверяемого файла.

    Returns:
        str: Ответ на вопрос, лежит ли по указанному пути файл.
    """
    return os.path.isfile(filepath)

def delete_file(filepath: str) -> None:
    """
    

    Args:
        filepath (str): _description_
    """
    if object_is_file(filepath=filepath):
        os.remove(filepath)