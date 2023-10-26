import os

from . import file_exceptions


class FileManager:

    def object_is_file(self, filepath: str) -> bool:
        """
        Утилита которая проверяется, является ли объект файлом.

        Args:

            filepath (str): Путь проверяемого объекта.

        Returns:
            bool: Ответ, лежит ли по указанному пути файл.

        Raises:
            file_exceptions.NoPathEntity: Ошибка, если передан не путь.
        """
        if isinstance(filepath, str):
            return os.path.isfile(filepath)
        raise file_exceptions.NoPathEntity(value=filepath)

    def delete_file(self, filepath: str) -> None:
        """
        Утилита которая удаляет файл.

        Args:

            - filepath (str): Путь удаляемого файла.

        Raises:
            file_exceptions.NotSuccessDeleteFileEntity: Ошибка,
                если после удаления файл существует.
            file_exceptions.DeleteNotExistFileEntity: Ошибка,
                если такого файла не существует.
        """
        if self.object_is_file(filepath=filepath):
            os.remove(filepath)
            if self.object_is_file(filepath=filepath):
                raise file_exceptions.NotSuccessDeleteObjectEntity(
                    path=filepath
                )
        else:
            raise file_exceptions.DeleteNotExistObjectEntity(path=filepath)

    def file_not_exist(self, filepath):
        if self.object_is_file(filepath=filepath):
            raise file_exceptions.FileAlreadyExistEntity(path=filepath)

    def write_to_new_file_text(self, filepath, data):
        self.file_not_exist(filepath=filepath)
        with open(file=filepath, mode='w') as f:
            f.write(data)

    def write_to_new_file_binary(self, filepath, data):
        self.file_not_exist(filepath=filepath)
        with open(file=filepath, mode='wb') as f:
            f.write(data)
