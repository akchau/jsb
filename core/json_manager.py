import json
import os

from core.file_manger import object_is_file


def object_is_json_file(filepath: str) -> bool:
    """
    Утилита которая проверяется, является ли объект json-файлом.

    Args:
        filepath (str): _description_

    Returns:
        bool: _description_
    """
    if object_is_file(filepath=filepath) and filepath.endswith(".json"):
        return True
    else:
        return False


def load_dict_in_json(filepath: str, data: dict) -> None:
    """
    Утилита, которая загружает в json-файл словарь.

    Args:

        - filepath (str): Путь файла, в который будет загружаться словарь

        - data (dict): Словарь.
    """
    if not object_is_json_file(filepath=filepath):
        with open(file=filepath, mode="w", encoding='utf-8') as new_json:
            json.dump(data, new_json, indent=4, ensure_ascii=False)


def read_json(filepath: str) -> dict:
    """
    Утилита которая возвращает содержимое json-файла.

    Args:
        filepath (str): Путь json-файла.

    Returns:
        dict: Содержимое json-файла.
    """
    if object_is_json_file(filepath=filepath):
        try:
            with open(file=filepath, mode='r', encoding='utf-8') as json_file:
                data = json.load(json_file)
            return data
        except json.decoder.JSONDecodeError:
            return None
    return None


def read_dict_in_json(filepath: str) -> dict:
    data = read_json(filepath=filepath)
    if isinstance(data, dict):
        return data
    return None


class BaseJsonController:

    LIST_OF_FILENAMES = "data/system/shedule_cache/list_of_filenames.json"
    BASE_SCHEDULE_PATH = "data/system/shedule_cache/objects"

    def _get_json_record(self, filepath, key):
        json_dict = read_dict_in_json(filepath=filepath)
        return json_dict.get(key)

    def _write_json_record(self, filepath, key, value):
        data = read_json(filepath=filepath)
        if isinstance(data, dict):
            if data.get(key):
                del data[key]
        data[key] = value
        load_dict_in_json(
            data=data,
            filepath=filepath
        )

    def _create_new_filepath(self, filename):
        return os.path.join(self.BASE_SCHEDULE_PATH, f"{filename}.json")
