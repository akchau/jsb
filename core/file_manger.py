import os


def object_is_file(filepath: str):
    return os.path.isfile(filepath)

def delete_file(filepath: str):
    return os.remove(filepath)