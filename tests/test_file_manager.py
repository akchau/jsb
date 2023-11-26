# import json
import os
import shutil
import unittest

from core.file_manager.file_manager import FileManager
from core.file_manager import file_exceptions

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestClass:
    def __str__(self) -> str:
        return "Я тестовый класс!"


class TestObjectIsFile(unittest.TestCase):

    __NON_EXIST_FILENAME = "non_exist.txt"
    __EXIST_FILENAME = "exist.txt"
    __EXIST_DIRNAME = "exist_dir"
    __NUMBER = 333
    __DICT = {"number": 333}
    __TUPLE = ("number", 333)
    __LIST = ["number", 333]

    @classmethod
    def setUpClass(cls) -> None:
        cls.NON_EXIST_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__NON_EXIST_FILENAME
        )

        cls.EXIST_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__EXIST_FILENAME
        )
        cls.EXIST_DIRPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__EXIST_DIRNAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.fm = FileManager()

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_non_exist_file(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Несуществующий путь.
        """
        self.assertFalse(self.fm.object_is_file(self.NON_EXIST_FILEPATH))

    def test_with_exist_file(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующий файл.
        """
        with open(self.EXIST_FILEPATH, 'w+'):
            pass
        self.assertTrue(self.fm.object_is_file(self.EXIST_FILEPATH))

    def test_with_exist_dir(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующая директория.
        """
        os.mkdir(self.EXIST_DIRPATH)
        self.assertFalse(self.fm.object_is_file(self.EXIST_DIRPATH))

    def test_with_number(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Целое число.
        """
        with self.assertRaises(file_exceptions.NoPathEntity) as context:
            self.fm.object_is_file(filepath=self.__NUMBER)
            self.assertEqual(
                context.exception,
                f"Переданное значение не является путем - {self.__NUMBER}"
            )

    def test_with_dict(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Словарь.
        """
        with self.assertRaises(file_exceptions.NoPathEntity) as context:
            self.fm.object_is_file(filepath=self.__DICT)
            self.assertEqual(
                context.exception,
                f"Переданное значение не является путем - {self.__DICT}"
            )

    def test_with_tuple(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Кортеж.
        """
        with self.assertRaises(file_exceptions.NoPathEntity) as context:
            self.fm.object_is_file(filepath=self.__TUPLE)
            self.assertEqual(
                context.exception,
                f"Переданное значение не является путем - {self.__TUPLE}"
            )

    def test_with_list(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Список.
        """
        with self.assertRaises(file_exceptions.NoPathEntity) as context:
            self.fm.object_is_file(filepath=self.__LIST)
            self.assertEqual(
                context.exception,
                f"Переданное значение не является путем - {self.__LIST}"
            )

    def test_with_class(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Класс.
        """
        self.assertRaises(
            file_exceptions.NoPathEntity,
            self.fm.object_is_file,
            TestClass
        )

    def test_with_class_object(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        self.assertRaises(
            file_exceptions.NoPathEntity,
            self.fm.object_is_file,
            TestClass()
        )

    def test_with_none(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        with self.assertRaises(file_exceptions.NoPathEntity) as context:
            self.fm.object_is_file(filepath=None)
            self.assertEqual(
                context.exception,
                f"Переданное значение не является путем - {None}"
            )


class TestDeleteFile(unittest.TestCase):
    __FILENAME = "exist.txt"

    @classmethod
    def setUpClass(cls) -> None:
        cls.FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.fm = FileManager()

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_non_exist_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Несуществующий файл.
        """
        with self.assertRaises(
           file_exceptions.FileNotYetExistException) as context:
            self.fm.delete_file(
                filepath=self.FILEPATH
            )
            self.assertEqual(
                context.exception,
                f"Файл {self.FILEPATH} не существует.")

    def test_with_exist_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Существующий файл.
        """
        with open(self.FILEPATH, 'w+'):
            pass
        self.assertTrue(self.fm.object_is_file(self.FILEPATH))
        self.fm.delete_file(self.FILEPATH)
        self.assertFalse(self.fm.object_is_file(self.FILEPATH))

    def test_without_rights_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Существующий открытый файл.
        """
        with open(self.FILEPATH, 'w+'):
            pass
        os.chmod(self.FILEPATH, 0o000)
        self.assertTrue(os.path.isfile(self.FILEPATH))
        self.fm.delete_file(self.FILEPATH)
        self.assertFalse(os.path.isfile(self.FILEPATH))


class TestWriteToNewFile(unittest.TestCase):
    __FILENAME = "exist.txt"

    @classmethod
    def setUpClass(cls) -> None:
        cls.FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.fm = FileManager()

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_write_to_not_exist_file(self):
        self.fm.write_to_new_file_text(self.FILEPATH, "Тестовый текст")

    def test_write_to_exist_file(self):
        with open(self.FILEPATH, 'w+'):
            pass
        with self.assertRaises(
           file_exceptions.FileAlreadyExistException) as context:
            self.fm.write_to_new_file_text(
                filepath=self.FILEPATH,
                data="Тестовый текст"
            )
            self.assertEqual(
                context.exception,
                f"Такой файл уже существует - {self.FILEPATH}",
            )
