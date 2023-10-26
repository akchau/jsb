import json
import os
import fcntl

from ..file_manager.file_manager import FileManager
from .import json_exceptions


class JsonFileManager(FileManager):

    def __init__(self, filepath):
        self.__lockfile = "lockfile" + ".lock"
        self.filepath = filepath

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        """Сеттер для пути json-файла"""
        if isinstance(value, str) and value.endswith(".json"):
            self._filepath = value
        else:
            raise json_exceptions.NotJsonPathEntity(value=value)

    def _json_file_exist(self) -> bool:
        """
        Утилита которая проверяется, является ли объект json-файлом.

        Args:
            filepath (str): Путь json-файла.

        Returns:
            bool: Ответ.
        """
        if self.object_is_file(filepath=self.filepath):
            return True
        else:
            return False

    def _acquire_lock(self):
        try:
            self.lock_fd = open(self.__lockfile, 'w')
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, IOError):
            raise json_exceptions.AnotherProcessLockFileEntity

    def _release_lock(self):
        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
        self.lock_fd.close()

    def _overwrite_data_in_json(self, data) -> None:
        if self._json_file_exist():
            self._load_data_in_json(data=data)
        else:
            raise json_exceptions.NotExistEntity(path=self.filepath)

    def _create_new_json_with_data(self, data) -> None:
        if not self._json_file_exist():
            self._load_data_in_json(data=data)
        else:
            raise json_exceptions.AlreadyExistEntity(path=self.filepath)

    def _load_data_in_json(self, data) -> None:
        """
        Утилита, которая загружает в json-файл словарь.

        Args:

            - filepath (str): Путь файла, в который будет загружаться словарь

            - data (dict): Словарь.
        """
        try:
            self._acquire_lock()
            with open(file=self.filepath, mode="w",
                      encoding='utf-8') as new_json:
                json.dump(data, new_json, indent=4, ensure_ascii=False)
        except PermissionError:
            raise json_exceptions.NotPermissionForWriteEntity
        finally:
            self._release_lock()

    def _read_json(self) -> dict:
        """
        Утилита которая возвращает содержимое json-файла.

        Args:
            filepath (str): Путь json-файла.

        Raises:
            json_exceptions.EmptyJsonEntity: Если файл пустой.
            json_exceptions.NotPermissionForReadEntity:
                Если нет прав на чтение.
            json_exceptions.NotJsonEntity: Если не является json-файлом.

        Returns:
            dict: Содержимое json-файла.
        """
        if self._json_file_exist():
            try:
                self._acquire_lock()
                with open(file=self.filepath, mode='r',
                          encoding='utf-8') as json_file:
                    data = json.load(json_file)
                return data
            except json.decoder.JSONDecodeError:
                if os.stat(self.filepath).st_size == 0:
                    raise json_exceptions.EmptyJsonEntity(path=self.filepath)
            except PermissionError:
                raise json_exceptions.NotPermissionForReadEntity
            finally:
                self._release_lock()
        else:
            raise json_exceptions.NotExistEntity(path=self.filepath)

    def _overwrite_dict_in_json(self, data: dict):
        if isinstance(data, dict):
            self._overwrite_data_in_json(
                data=data
            )
        else:
            raise json_exceptions.DataIsNotDictEntity(
                path=self.filepath,
                data=data
            )

    def _read_dict_from_json(self) -> dict:
        data = self._read_json()
        if isinstance(data, dict):
            return data
        else:
            raise json_exceptions.DataIsNotDictEntity(
                path=self.filepath,
                data=data
            )

    def _check_keys_tuple(self, keys: tuple) -> None:
        for dict_key in keys:
            if not isinstance(dict_key, (int, str, tuple, frozenset)):
                raise json_exceptions.NotValideTypeForKey(value=dict_key)

    def _read_dict_record_from_json(self, keys: tuple):
        json_data_dict = self._read_dict_from_json()
        self.check_keys_tuple(keys=keys)
        result = json_data_dict
        for dict_key in keys:
            try:
                result = result[dict_key]
            except KeyError:
                raise json_exceptions.KeyNotExistInJsonDict(
                    path=self.filepath,
                    key=dict_key
                )
        return result


# class JsonDB(JsonFileManager):




class BaseJsonController(JsonFileManager):

    LIST_OF_FILENAMES = "data/system/shedule_cache/list_of_filenames.json"
    BASE_SCHEDULE_PATH = "data/system/shedule_cache/objects"

    def _get_json_record(self, filepath, key):
        json_dict = self.read_dict_in_json(filepath=filepath)
        return json_dict.get(key)

    def _write_json_record(self, filepath, key, value):
        data = self.read_dict_in_json(filepath=filepath)
        if isinstance(data, dict):
            if data.get(key):
                del data[key]
        data[key] = value
        self.load_dict_in_json(
            data=data,
            filepath=filepath
        )

    def _create_new_filepath(self, filename):
        return os.path.join(self.BASE_SCHEDULE_PATH, f"{filename}.json")
