import os
import shutil
import unittest

from core.file_manger import object_is_file


class TestCoreFileManger(unittest.TestCase):

    MODULE_PATH = os.path.abspath(__file__)
    TEMP_FIXTURE_DIRPATH = os.path.join(os.path.dirname(MODULE_PATH), "__fixture__")

    def setUp(self) -> None:
        os.mkdir(self.TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        shutil.rmtree(self.TEMP_FIXTURE_DIRPATH)

    def test_object_non_file(self):
        NON_EXIST_FILENAME = "non_exist.txt"
        NON_EXIST_FILEPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            NON_EXIST_FILENAME
        )
        self.assertFalse(object_is_file(NON_EXIST_FILEPATH))

    def test_object_file(self):
        EXIST_FILENAME = "exist.txt"
        EXIST_FILEPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            EXIST_FILENAME
        )
        with open(EXIST_FILEPATH, 'w+') as file:
            pass
        self.assertTrue(object_is_file(EXIST_FILEPATH))