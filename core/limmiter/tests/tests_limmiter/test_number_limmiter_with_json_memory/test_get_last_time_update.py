from datetime import datetime
import os
import shutil
import unittest

from ....limmiter import NumberLimmiterWithJsonMemory

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestGetValue(unittest.TestCase):
    MEMORY_FILENAME = "memory.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.MEMORY_PATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.MEMORY_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        if os.path.isdir(TEMP_FIXTURE_DIRPATH):
            shutil.rmtree(TEMP_FIXTURE_DIRPATH)
        os.mkdir(TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_value(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        self.assertEqual(limmiter.get_last_update_time(), datetime.now().strftime("%Y-%m-%d %H:%M"))

    def test_last_day_update_is_today(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        last_update_time = datetime.strptime(limmiter.get_last_update_time(), "%Y-%m-%d %H:%M")
        is_today = (last_update_time.date() == datetime.now().date())
        self.assertTrue(is_today)
