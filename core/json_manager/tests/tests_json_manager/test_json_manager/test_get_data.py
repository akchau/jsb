import json
import os
import shutil
import unittest

from ....json_manager import JsonFileManager

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
    TEXT_FILENAME = "exist.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEXT_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.TEXT_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        if os.path.isdir(TEMP_FIXTURE_DIRPATH):
            shutil.rmtree(TEMP_FIXTURE_DIRPATH)
        os.mkdir(TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_without_create(self) -> None:
        NEW_DATA = "Данные"
        self.assertFalse(os.path.isfile(path=self.TEXT_FILEPATH))
        with open(file=self.TEXT_FILEPATH, mode="w", encoding='utf-8') as new_json:
            json.dump(
                NEW_DATA,
                new_json,
                indent=4,
                ensure_ascii=False
            )
        data = self.memory = JsonFileManager(
            path=self.TEXT_FILEPATH,
            destroy=False,
            create=True
        ).get_data()
        self.assertEqual(data, NEW_DATA)
