import os

from ..base_manager.base_manager import BaseTypeManager
from .file_exceptions import (
    FileNotYetExistException,
    FileAlreadyExistException,
    NotSucsessCreateFile,
    NotSuccessDeleteObjectEntity
)


class FileManager(BaseTypeManager):

    def __init__(self, path: str, destroy: bool = False,
                 create: bool = False) -> None:
        self.path = self.slice_path(value=path)
        if self.validate_bool(create) is True:
            try:
                self.create_new_file()
            except Exception:
                raise NotSucsessCreateFile()
        self.destroy = self.validate_bool(data=destroy)
        self.deleted = False

    def create_new_file(self):
        if not os.path.isfile(path=self.path):
            self.write(data='', mode="w")
        else:
            raise FileAlreadyExistException(path=self.path)

    def __del__(self):
        if self.destroy and not self.deleted:
            self.delete()

    def delete(self) -> None:
        """
        Утилита которая удаляет файл.

        Args:

            - filepath (str): Путь удаляемого файла.

        Raises:

            file_exceptions.NotSuccessDeleteFileEntity: Ошибка,
                если после удаления файл существует.
        """
        if not self.deleted:
            os.remove(self.exist_path)
        if os.path.isfile(self.path):
            raise NotSuccessDeleteObjectEntity(
                path=self.path
            )

    def write(self, data, mode):
        if not self.deleted:
            with open(file=self.exist_path, mode=mode) as f:
                f.write(data)

    @property
    def exist_path(self):
        if os.path.isfile(self.path):
            return self.path
        raise FileNotYetExistException(path=self.path)
