import json
import os
import shutil
import unittest

from ...number_request_controller import NumberRequestControler


MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestApiRequestPermission(unittest.TestCase):
    """
    Тестирование функции _json_file_exist

    Тесты:

    - test_with_exist_json_file - Тестирование с путем
        существующего json-файла.

    - test_with_not_exist_json_file - Тестирование с путем несуществующего
        json-файла.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.TEST_MEMORY_PATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            "number_trying_day.json"
        )
        cls.MAX_TRYING = 10

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        if os.path.isdir(TEMP_FIXTURE_DIRPATH):
            shutil.rmtree(TEMP_FIXTURE_DIRPATH)
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.controller = NumberRequestControler(
            path=self.TEST_MEMORY_PATH,
            max_requests=self.MAX_TRYING
        )
        with open(file=self.TEST_MEMORY_PATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(
                {self.controller.LOST_TRYING_KEY: self.MAX_TRYING},
                new_json,
                indent=4,
                ensure_ascii=False
            )

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_exist_json_file(self):
        """
        Тестируемая функция:

        - _object_is_json_file()

        Тестируемое значение:

        - Путь json-файлa.
        """
        for _ in range(self.MAX_TRYING):
            self.assertTrue(self.controller.get_request_permission())
        self.assertFalse(self.controller.get_request_permission())
