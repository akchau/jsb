import os
from typing import Union

from core import exceptions as file_exceptions


class FileManager:

    def object_is_file(self, filepath: str) -> bool:
        """
        Утилита которая проверяется, является ли объект файлом.

        Args:

            filepath (str): Путь проверяемого файла.

        Returns:

            str: Ответ на вопрос, лежит ли по указанному пути файл.
        """
        if isinstance(filepath, str):
            return os.path.isfile(filepath)
        raise file_exceptions.NoPathEntity

    def delete_file(self, filepath: str) -> Union[str, None]:
        """
        Утилита которая удаляет файл.

        Args:

            - filepath (str): Путь удаялемого файла.
        Returns:

            - Union[str, None]: Если файл удален - путь файла, или None.
        """
        if self.object_is_file(filepath=filepath):
            os.remove(filepath)
            if self.object_is_file(filepath=filepath):
                raise file_exceptions.NotSuccessDeleteFileEntity
        else:
            raise file_exceptions.DeleteNotExistFileEntity
