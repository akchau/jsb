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

    def test_use_all_trying(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        for _ in range(FULL_NUMBER):
            self.assertTrue(limmiter.use_trying())
        self.assertEqual(limmiter.get_memory_value(), 0)
        self.assertFalse(limmiter.use_trying())
        self.assertEqual(limmiter.get_memory_value(), 0)

    def test_use_trying_another_client(self):
        FULL_NUMBER = 100
        limmiter_one = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        self.assertTrue(limmiter_one.use_trying())
        self.assertEqual(limmiter_one.get_memory_value(), FULL_NUMBER - 1)
        limmiter_one = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        self.assertTrue(limmiter_one.use_trying())
        self.assertEqual(limmiter_one.get_memory_value(), FULL_NUMBER - 2)
