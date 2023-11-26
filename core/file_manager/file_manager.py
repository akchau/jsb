import os

from .file_exceptions import (
    FileNotYetExistException,
    NoPathEntity,
    NotSucsessCreateFile,
    NotSuccessDeleteObjectEntity
)


class FileManager:

    def __init__(self, path: str, destroy: bool = False,
                 create: bool = False) -> None:
        if create is True:
            try:
                if os.path.isfile(self.path_validator(value=path)):
                    self.create_new_file(path=path)
            except Exception:
                raise NotSucsessCreateFile()
        self.path = self.path_validator(value=path)
        self.destroy = destroy
        self.deleted = False

    def create_new_file(self, path: str):
        if not os.path.isfile(path=path):
            self.write(data='', mode="w")

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

    def path_validator(self, value: str):
        if isinstance(value, str):
            return value.strip()
        else:
            raise NoPathEntity(value=value)
