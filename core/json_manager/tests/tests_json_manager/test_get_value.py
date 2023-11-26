import json
import os
import shutil
import unittest

from ...json_manager import JsonFileManager

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestGetCorrectValue(unittest.TestCase):
    """
    Тестирование функции _json_file_exist

    Тесты:

    - test_with_exist_json_file - Тестирование с путем
        существующего json-файла.

    - test_with_not_exist_json_file - Тестирование с путем несуществующего
        json-файла.
    """
    EXIST_JSON_FILENAME = "exist.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.EXIST_JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.EXIST_JSON_FILENAME
        )
        cls.dict_key = "key"
        cls.dict_value = "value"

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        if os.path.isdir(TEMP_FIXTURE_DIRPATH):
            shutil.rmtree(TEMP_FIXTURE_DIRPATH)
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        with open(file=self.EXIST_JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(
                {self.dict_key: self.dict_value},
                new_json,
                indent=4,
                ensure_ascii=False
            )
        self.memory = JsonFileManager(
            path=self.EXIST_JSON_FILEPATH,
            destroy=False,
            create=False
        )

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_get_correct_value(self):
        """
        Тестируемая функция:

        - _object_is_json_file()

        Тестируемое значение:

        - Путь json-файлa.
        """
        self.assertTrue(
            self.memory.get_value(
                parse_keys=(
                    (
                        self.dict_key,
                        str
                    ),
                )
            )
        )
