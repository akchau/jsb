from datetime import datetime
import json
import os
from typing import Any

from ..file_manager.file_manager import FileManager
from .json_exceptions import (
    EmptyJsonException,
    FileNotYetExistException,
    NotJsonPathException,
    NotSucsessWriteDataToFile
)


class JsonFileManager(FileManager):
    """
    Класс управления json-файлом.
    """

    def validate_path(self, value: str) -> str:
        """
        Метод проверки пути.

        Args:
            value (str): Значение передаваемое в качестве пути.

        Returns:
            str: Возвращаемое знчение.
        """
        clean_string = self.validate_str(data=value)
        if clean_string.endswith(".json"):
            return clean_string
        raise NotJsonPathException(value=value)

    def write_data(self, data: Any) -> None:
        with open(file=self.path, mode="w", encoding='utf-8') as new_json:
            json.dump(
                data,
                new_json,
                indent=4,
                ensure_ascii=False
            )
        writed_data = self.get_data()
        if writed_data != data:
            raise NotSucsessWriteDataToFile(path=self.path, data=data)

    def get_data(self) -> Any:
        """
        Утилита которая возвращает содержимое json-файла.

        Args:
            filepath (str): Путь json-файла.

        Raises:
            json_exceptions.EmptyJsonException: Если файл пустой.
            json_exceptions.NotPermissionForReadException:
                Если нет прав на чтение.
            json_exceptions.NotJsonEntity: Если не является json-файлом.

        Returns:
            dict: Содержимое json-файла.
        """
        if self.file_exist():
            try:
                with open(file=self.path, mode='r',
                          encoding='utf-8') as json_file:
                    return json.load(json_file)
            except json.decoder.JSONDecodeError as e:
                if os.stat(self.path).st_size == 0:
                    raise EmptyJsonException(path=self.path)
                else:
                    raise e
        raise FileNotYetExistException(path=self.path)
