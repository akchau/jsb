import os

from . import file_exceptions


class FileManager:

    def object_is_file(self, filepath: str) -> bool:
        """
        Утилита которая проверяется, является ли объект файлом.

        Args:

            filepath (str): Путь проверяемого файла.

        Returns:
            bool: Ответ, лежит ли по указанному пути файл.

        Raises:
            file_exceptions.NoPathEntity: Ошибка, если передан не путь файла.
        """
        if isinstance(filepath, str):
            return os.path.isfile(filepath)
        raise file_exceptions.NoPathEntity

    def delete_file(self, filepath: str) -> None:
        """
        Утилита которая удаляет файл.

        Args:

            - filepath (str): Путь удаялемого файла.

        Raises:
            file_exceptions.NotSuccessDeleteFileEntity: Ошибка,
                если после удаления файл существует.
            file_exceptions.DeleteNotExistFileEntity: Ошибка,
                если такого файла не существует.
        """
        if self.object_is_file(filepath=filepath):
            os.remove(filepath)
            if self.object_is_file(filepath=filepath):
                raise file_exceptions.NotSuccessDeleteFileEntity
        else:
            raise file_exceptions.DeleteNotExistFileEntity
