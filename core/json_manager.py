import json

from j_bot.core.file_manger import object_is_file


def load_dict_in_json(filepath: str, data: dict):
    if object_is_file(filepath=filepath):
        with open(file=filepath, mode="w") as new_json:
            json.dumps(data, new_json, indent=4)
