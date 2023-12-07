import os
import shutil
import unittest

from ....json_manager import JsonFileManager

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestDestroy(unittest.TestCase):
    """
    Тестирование удаления после использования.

    Тесты:

    - test_without_destroy - Тестирование без удаления файла.

    - test_with_destroy - Тестирование с путем несуществующего
        json-файла.
    """
    EXIST_TEXT_FILENAME = "exist.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.EXIST_TEXT_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.EXIST_TEXT_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        if os.path.isdir(TEMP_FIXTURE_DIRPATH):
            shutil.rmtree(TEMP_FIXTURE_DIRPATH)
        os.mkdir(TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_without_destroy(self) -> None:
        self.memory = JsonFileManager(
            path=self.EXIST_TEXT_FILEPATH,
            destroy=False,
            create=True
        )
        del self.memory
        self.assertTrue(os.path.isfile(path=self.EXIST_TEXT_FILEPATH))

    def test_with_destroy(self) -> None:
        self.memory = JsonFileManager(
            path=self.EXIST_TEXT_FILEPATH,
            destroy=True,
            create=True
        )
        del self.memory
        self.assertFalse(os.path.isfile(path=self.EXIST_TEXT_FILEPATH))
