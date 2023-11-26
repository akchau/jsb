from datetime import date, datetime, timedelta
import json
import os
import time
from typing import Any

from ..dict_manager.dict_manager import validate_dict, parse_dict
from ..file_manager.file_manager import FileManager
from .json_exceptions import EmptyJsonException, NotJsonPathException, NotSucsessCreateFile


class JsonFileManager(FileManager):

    LAST_TIME_UPDATE_KEY = "last_update"
    START_DICT = {}

    def __init__(self, path: str, destroy: bool = False,
                 create: bool = False) -> None:
        if create is True:
            try:
                if os.path.isfile(self.path_validator(value=path)):
                    self.create_new_file(
                        path=path,
                        start_data=self.START_DICT
                    )
            except Exception:
                raise NotSucsessCreateFile()
        self.path = self.path_validator(value=path)
        self.destroy = destroy
        self.deleted = False

    @property
    def json_path(self):
        if self.path.endswith(".json"):
            return self.exist_path
        else:
            raise NotJsonPathException(value=self.exist_path)

    def create_new_file(self, path: str, start_data):
        start_data: dict = validate_dict(data=start_data)
        with open(file=path, mode="w", encoding='utf-8') as new_json:
            json.dump(
                start_data,
                new_json,
                indent=4,
                ensure_ascii=False
            )

    def _service_info(self) -> dict:
        return {self.LAST_TIME_UPDATE_KEY: str(datetime.now())}

    def write(self, data: dict) -> None:
        """
        Утилита, которая загружает в json-файл словарь.

        Args:

            - filepath (str): Путь файла, в который будет загружаться словарь

            - data (dict): Словарь.
        """
        clean_data: dict = validate_dict(data)
        clean_data.update(self._service_info())
        self.create_new_file(path=self.json_path, start_data=data)

    def get_value(self, parse_keys: tuple) -> Any:
        return parse_dict(
            data=self._read_json(),
            parse_keys=parse_keys
        )

    def get_last_time_update(self) -> datetime:
        return parse_dict(
            data=self._read_json(),
            parse_keys=((self.LAST_TIME_UPDATE_KEY, datetime.datetime),)
        )

    def _read_json(self) -> dict:
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
        try:
            with open(file=self.json_path, mode='r',
                      encoding='utf-8') as json_file:
                return json.load(json_file)
        except json.decoder.JSONDecodeError as e:
            if os.stat(self.json_path).st_size == 0:
                raise EmptyJsonException(path=self.json_path)
            else:
                raise e
