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

    def test_set_number_with_correct_value(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        limmiter.set_actual_number_of_trying(new_value=3)
        self.assertEqual(limmiter.get_memory_value(), 3)

    def test_set_number_with_to_big_value(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        limmiter.use_trying()
        limmiter.set_actual_number_of_trying(new_value=150)
        self.assertEqual(limmiter.get_memory_value(), FULL_NUMBER)

    def test_set_number_without_value(self):
        FULL_NUMBER = 100
        limmiter = NumberLimmiterWithJsonMemory(
            memory_path=self.MEMORY_PATH,
            full_number=FULL_NUMBER
        )
        limmiter.use_trying()
        limmiter.set_actual_number_of_trying()
        self.assertEqual(limmiter.get_memory_value(), FULL_NUMBER)
