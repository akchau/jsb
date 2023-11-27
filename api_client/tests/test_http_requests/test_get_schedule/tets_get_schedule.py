import json
import os
import shutil
import unittest

from ....number_request_controller import NumberRequestControler
from ....http_requests.get_schedule import get_schedule


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

    def test_with_good_case(self):
        """
        Тестируемая функция:

        - _object_is_json_file()

        Тестируемое значение:

        - Путь json-файлa.
        """
        self.assertEqual(get_schedule(), {})
