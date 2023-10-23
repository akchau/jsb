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
            filepath (str): _description_

        Returns:
            bool: _description_
        """
        if self.object_is_file(filepath=filepath) and filepath.endswith(".json"):
            return True
        else:
            return False

    def acquire_lock(self):
        # Попытка получения эксклюзивной блокировки
        try:
            self.lock_fd = open(self.lockfile, 'w')
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, IOError):
            # Не удалось получить блокировку, файл заблокирован другим процессом
            raise Exception("Cannot acquire lock. Another process is using the file.")

    def release_lock(self):
        # Освобождение блокировки
        fcntl.flock(self.lock_fd, fcntl.LOCK_UN)
        self.lock_fd.close()

    def load_data_in_json(self, filepath: str, data) -> None:
        """
        Утилита, которая загружает в json-файл словарь.

        Args:

            - filepath (str): Путь файла, в который будет загружаться словарь

            - data (dict): Словарь.
        """
        if (self.object_is_json_file(filepath=filepath) or not
           self.object_is_file(filepath=filepath)):
            with open(file=filepath, mode="w", encoding='utf-8') as new_json:
                json.dump(data, new_json, indent=4, ensure_ascii=False)
        else:
            raise json_exceptions.AlreadyExistNotJsonEntity

    def load_dict_in_json(self, filepath: str, data: dict):
        if isinstance(data, dict):
            self.load_data_in_json(
                filepath=filepath,
                data=data
            )
        else:
            raise json_exceptions.DataIsNotDictEntity

    def read_json(self, filepath: str) -> dict:
        """
        Утилита которая возвращает содержимое json-файла.

        Args:
            filepath (str): Путь json-файла.

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
        data = self.read_json(filepath=filepath)
        if isinstance(data, dict):
            return data
        return None


class BaseJsonController(JsonManager):

    LIST_OF_FILENAMES = "data/system/shedule_cache/list_of_filenames.json"
    BASE_SCHEDULE_PATH = "data/system/shedule_cache/objects"

    def _get_json_record(self, filepath, key):
        json_dict = self.read_dict_in_json(filepath=filepath)
        return json_dict.get(key)

    def _write_json_record(self, filepath, key, value):
        data = self.read_json(filepath=filepath)
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
