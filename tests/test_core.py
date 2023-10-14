import os
import shutil
import unittest

from core.file_manger import delete_file, object_is_file


class TestClass:
    def __str__(self) -> str:
        return "Я тестовый класс!"


class TestCoreFileManger(unittest.TestCase):

    MODULE_PATH = os.path.abspath(__file__)
    TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(self.TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(self.TEMP_FIXTURE_DIRPATH)

    def test_object_is_file_with_non_exist_file(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Несуществующий путь.
        """
        NON_EXIST_FILENAME = "non_exist.txt"
        NON_EXIST_FILEPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            NON_EXIST_FILENAME
        )
        self.assertFalse(object_is_file(NON_EXIST_FILEPATH))

    def test_object_is_file_with_exist_file(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующий файл.
        """
        EXIST_FILENAME = "exist.txt"
        EXIST_FILEPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            EXIST_FILENAME
        )
        with open(EXIST_FILEPATH, 'w+'):
            pass
        self.assertTrue(object_is_file(EXIST_FILEPATH))

    def test_object_is_file_with_exist_dir(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующая директория.
        """
        EXIST_DIRNAME = "exist_dir"
        EXIST_DIRPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            EXIST_DIRNAME
        )
        os.mkdir(EXIST_DIRPATH)
        self.assertFalse(object_is_file(EXIST_DIRPATH))

    def test_object_is_file_with_number(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Целое число.
        """
        NUMBER = 333
        self.assertFalse(object_is_file(NUMBER))

    def test_object_is_file_with_dict(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Словарь.
        """
        DICT = {"number": 333}
        self.assertFalse(object_is_file(DICT))

    def test_object_is_file_with_tuple(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Кортеж.
        """
        TUPLE = ("number", 333)
        self.assertFalse(object_is_file(TUPLE))

    def test_object_is_file_with_list(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Список.
        """
        LIST = ["number", 333]
        self.assertFalse(object_is_file(LIST))

    def test_object_is_file_with_class(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Класс.
        """
        self.assertFalse(object_is_file(TestClass))

    def test_object_is_file_with_class_object(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        self.assertFalse(object_is_file(TestClass()))

    def test_object_is_file_with_none(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        self.assertFalse(object_is_file(None))


class TestDeleteFile(unittest.TestCase):

    MODULE_PATH = os.path.abspath(__file__)
    TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(self.TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(self.TEMP_FIXTURE_DIRPATH)

    def test_delete_file_with_non_exist_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Несуществующий путь.
        """
        NON_EXIST_FILENAME = "non_exist.txt"
        NON_EXIST_FILEPATH = os.path.join(
            self.TEMP_FIXTURE_DIRPATH,
            NON_EXIST_FILENAME
        )
        self.assertIsNone(delete_file(NON_EXIST_FILEPATH))
