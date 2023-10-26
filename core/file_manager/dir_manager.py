import os
import shutil

from . import file_exceptions


class DirManager:

    def object_is_dir(self, dirpath: str) -> bool:
        """
        Утилита которая проверяется, является ли объект директорией.

        Args:

            dirpath (str): Путь проверяемого объекта.

        Returns:
            bool: Ответ, лежит ли по указанному пути директория.

        Raises:
            file_exceptions.NoPathEntity: Ошибка, если передан не путь.
        """
        if isinstance(dirpath, str):
            return os.path.isdir(dirpath)
        raise file_exceptions.NoPathEntity(value=dirpath)

    def delete_dir(self, dirpath: str) -> None:
        """
        Утилита которая удаляет директорию.

        Args:

            - filepath (str): Путь удаляемой директории.

        Raises:
            file_exceptions.NotSuccessDeleteObjectEntity: Ошибка,
                если после удаления директория существует.
            file_exceptions.DeleteNotExistObjectEntity: Ошибка,
                если такой директории не существует.
        """
        if self.object_is_dir(dirpath=dirpath):
            shutil.rmtree(path=dirpath)
            if self.object_is_dir(dirpath=dirpath):
                raise file_exceptions.NotSuccessDeleteObjectEntity(
                    path=dirpath
                )
        else:
            raise file_exceptions.DeleteNotExistObjectEntity(path=dirpath)
