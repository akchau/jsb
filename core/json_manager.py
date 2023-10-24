import json
import os
import fcntl

from core.file_manger import FileManager
from core.json_manger import json_exceptions


class JsonManager(FileManager):

    def __init__(self):
        self.lockfile = "lockfile" + ".lock"

    def object_is_json_file(self, filepath: str) -> bool:
        """
        Утилита которая проверяется, является ли объект json-файлом.

        Args:
            filepath (str): Путь json-файла.

        Returns:
            bool: Ответ.
        """
        if self.object_is_file(filepath=filepath) and filepath.endswith(".json"):
            return True
        else:
            return False

    def acquire_lock(self):
        try:
            self.lock_fd = open(self.lockfile, 'w')
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, IOError):
            raise json_exceptions.AnotherProcessLockFileEntity

    def release_lock(self):
        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
        self.lock_fd.close()

    def _load_data_in_json(self, filepath: str, data) -> None:
        """
        Утилита, которая загружает в json-файл словарь.

        Args:

            - filepath (str): Путь файла, в который будет загружаться словарь

            - data (dict): Словарь.
        """
        if (self.object_is_json_file(filepath=filepath) or not
           self.object_is_file(filepath=filepath)):
            try:
                self.acquire_lock()
                with open(file=filepath, mode="w", encoding='utf-8') as new_json:
                    json.dump(data, new_json, indent=4, ensure_ascii=False)
            except PermissionError:
                raise json_exceptions.NotPermissionForWriteEntity
            finally:
                self.release_lock()
        else:
            raise json_exceptions.AlreadyExistNotJsonEntity

    def load_dict_in_json(self, filepath: str, data: dict):
        if isinstance(data, dict):
            self._load_data_in_json(
                filepath=filepath,
                data=data
            )
        else:
            raise json_exceptions.DataIsNotDictEntity

    def _read_json(self, filepath: str) -> dict:
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
        if self.object_is_json_file(filepath=filepath):
            try:
                self.acquire_lock()
                with open(file=filepath, mode='r',
                          encoding='utf-8') as json_file:
                    data = json.load(json_file)
                return data
            except json.decoder.JSONDecodeError:
                if os.stat(filepath).st_size == 0:
                    raise json_exceptions.EmptyJsonEntity
            except PermissionError:
                raise json_exceptions.NotPermissionForReadEntity
            finally:
                self.release_lock()
        else:
            raise json_exceptions.NotJsonEntity

    def read_dict_in_json(self, filepath: str) -> dict:
        data = self._read_json(filepath=filepath)
        if isinstance(data, dict):
            return data
        else:
            raise json_exceptions.DataIsNotDictEntity


class BaseJsonController(JsonManager):

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
