import os
from typing import Any

from ..base_manager.base_manager import BaseTypeManager
from .file_exceptions import (
    FileNotYetExistException,
    NotTxtPathException,
    NotSucsessCreateFile,
    NotSuccessDeleteObjectEntity,
    NotSucsessWriteDataToFile
)


class FileManager(BaseTypeManager):
    """
    Класс управления текстовым файлом
    """

    def __init__(self, path: str, destroy: bool = False,
                 create: bool = True) -> None:
        self.path = self.validate_path(value=path)
        if self.validate_bool(create) is True:
            try:
                self.create_new_file()
            except Exception:
                raise NotSucsessCreateFile(path=path)
        self.destroy = self.validate_bool(data=destroy)

    def validate_path(self, value: str) -> str:
        """
        Метод проверки пути.

        Args:
            value (str): Значение передаваемое в качестве пути.

        Returns:
            str: Возвращаемое знчение.
        """
        clean_string = self.validate_str(data=value)
        if clean_string.endswith(".txt"):
            return clean_string
        raise NotTxtPathException(value=value)

    def file_exist(self) -> bool:
        """
        Проверка существует ли файл.

        Returns:
            bool: Существет ли файл.
        """
        return os.path.isfile(path=self.path)

    def create_new_file(self) -> None:
        """
        Метод создания файла.
        """
        if not self.file_exist():
            self.write_data(data='')

    def __del__(self) -> None:
        """
        Удаление файла после завершения работы с классом.

        Raises:
            NotSuccessDeleteObjectEntity: Ошибка, если не удалось удалить файл.
        """
        if self.destroy and self.file_exist():
            os.remove(self.path)
            if os.path.isfile(self.path):
                raise NotSuccessDeleteObjectEntity(
                    path=self.path
                )

    def write_data(self, data: Any) -> None:
        """
        Метод записи в файл.

        Args:
            data (Any): Данные для записи в файл.

        Raises:
            NotSucsessWriteDataToFile: Ошибка, если не удалось запсиать в файл.
        """
        with open(file=self.path, mode="w") as f:
            f.write(data)
        writed_data = self.get_data()
        if writed_data != data:
            raise NotSucsessWriteDataToFile(path=self.path, data=data)

    def get_data(self) -> Any:
        if self.file_exist():
            with open(file=self.path, mode='r') as f:
                data = f.read()
            return data
        raise FileNotYetExistException(path=self.path)
