import json
import os
import shutil
import unittest

from core.file_manger import delete_file, object_is_file
from core.json_manager import object_is_json_file, read_json

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestClass:
    def __str__(self) -> str:
        return "Я тестовый класс!"


class TestObjectIsFile(unittest.TestCase):

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)

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
        NON_EXIST_FILENAME = "non_exist.txt"
        NON_EXIST_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            NON_EXIST_FILENAME
        )
        self.assertFalse(object_is_file(NON_EXIST_FILEPATH))

    def test_with_exist_file(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующий файл.
        """
        EXIST_FILENAME = "exist.txt"
        EXIST_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            EXIST_FILENAME
        )
        with open(EXIST_FILEPATH, 'w+'):
            pass
        self.assertTrue(object_is_file(EXIST_FILEPATH))

    def test_with_exist_dir(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Существующая директория.
        """
        EXIST_DIRNAME = "exist_dir"
        EXIST_DIRPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            EXIST_DIRNAME
        )
        os.mkdir(EXIST_DIRPATH)
        self.assertFalse(object_is_file(EXIST_DIRPATH))

    def test_with_number(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Целое число.
        """
        NUMBER = 333
        self.assertFalse(object_is_file(NUMBER))

    def test_with_dict(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Словарь.
        """
        DICT = {"number": 333}
        self.assertFalse(object_is_file(DICT))

    def test_with_tuple(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Кортеж.
        """
        TUPLE = ("number", 333)
        self.assertFalse(object_is_file(TUPLE))

    def test_with_list(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Список.
        """
        LIST = ["number", 333]
        self.assertFalse(object_is_file(LIST))

    def test_with_class(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Класс.
        """
        self.assertFalse(object_is_file(TestClass))

    def test_with_class_object(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        self.assertFalse(object_is_file(TestClass()))

    def test_with_none(self):
        """
        Тестируемая функция:

        - object_is_file()

        Тестируемое значение:

        - Объект класса.
        """
        self.assertFalse(object_is_file(None))


class TestDeleteFile(unittest.TestCase):
    __FILENAME = "exist.txt"
    FILEPATH = os.path.join(
        TEMP_FIXTURE_DIRPATH,
        __FILENAME
    )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)

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
        self.assertIsNone(delete_file(self.FILEPATH))

    def test_with_exist_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Существующий файл.
        """
        with open(self.FILEPATH, 'w+'):
            pass
        self.assertTrue(object_is_file(self.FILEPATH))
        self.assertEqual(delete_file(self.FILEPATH), self.FILEPATH)
        self.assertFalse(object_is_file(self.FILEPATH))

    def test_with_exist_already_open_file(self):
        """
        Тестируемая функция:

        - delete_file()

        Тестируемое значение:

        - Существующий открытый файл.
        """
        with open(self.FILEPATH, 'w+'):
            self.assertTrue(object_is_file(self.FILEPATH))
            self.assertIsNone(delete_file(self.FILEPATH))
            self.assertTrue(object_is_file(self.FILEPATH))


class TestObjectIsJSONFile(unittest.TestCase):
    """
    Тестирование функции object_is_json_file

    Тесты
    - test_with_json_file - Тестирование с путем json-файла.
    - test_with_not_json_file - Тестирование с путем текстового файла.
    """
    __EXIST_JSON_FILENAME = "exist.json"
    __EXIST_TXT_FILENAME = "exist.txt"

    @classmethod
    def setUpClass(cls) -> None:
        cls.EXIST_JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__EXIST_JSON_FILENAME
        )
        cls.EXIST_TXT_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__EXIST_TXT_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_json_file(self):
        """
        Тестируемая функция:

        - object_is_json_file()

        Тестируемое значение:

        - Путь json-файлa.
        """

        with open(self.EXIST_JSON_FILEPATH, 'w+'):
            pass

        self.assertTrue(object_is_json_file(self.EXIST_JSON_FILEPATH))

    def test_with_not_json_file(self):
        """
        Тестируемая функция:

        - object_is_json_file()

        Тестируемое значение:

        - Путь текстового файла.
        """

        with open(self.EXIST_TXT_FILEPATH, 'w+'):
            pass

        self.assertFalse(object_is_json_file(self.EXIST_TXT_FILEPATH))


class TestReadJson(unittest.TestCase):
    """
    Тестирование функции read_json

    Тесты
    - test_with_dict - Тестирование с json-файлом в котором словарь.
    - test_with_list - Тестирование с json-файлом в котором список.
    - test_open_in_write_mode_json_with_dict - Тестирование с json-файлом,
      который открыт в режиме записи.
    - test_open_in_read_mode_json_with_dict - Тестирование с json-файлом,
      который открыт в режиме чтенния.
    """
    __JSON_FILENAME = "exist.json"
    JSON_FILEPATH = os.path.join(
        TEMP_FIXTURE_DIRPATH,
        __JSON_FILENAME
    )
    DICT_DATA = {"key": "value"}
    LIST_DATA = ["one", "two"]

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_dict(self):
        """
        Тестируемая функция:

        - read_json()

        Тестируемое значение:

        - json-файл cо словарем.
        """

        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.DICT_DATA, new_json, indent=4, ensure_ascii=False)

        self.assertEqual(read_json(self.JSON_FILEPATH), self.DICT_DATA)

    def test_with_list(self):
        """
        Тестируемая функция:

        - read_json()

        Тестируемое значение:

        - json-файл cо списком.
        """

        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.LIST_DATA, new_json, indent=4, ensure_ascii=False)

        self.assertEqual(read_json(self.JSON_FILEPATH), self.LIST_DATA)

    def test_open_in_write_mode_json_with_dict(self):
        """
        Тестируемая функция:

        - read_json()

        Тестируемое значение:

        - Уже открытый json-файл в режиме записи.
        """

        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.DICT_DATA, new_json, indent=4, ensure_ascii=False)

        with open(file=self.JSON_FILEPATH, mode="w"):
            self.assertIsNone(read_json(self.JSON_FILEPATH))

    def test_open_in_read_mode_json_with_dict(self):
        """
        Тестируемая функция:

        - read_json()

        Тестируемое значение:

        - Уже открытый json-файл в режиме чтения.
        """

        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.DICT_DATA, new_json, indent=4, ensure_ascii=False)

        with open(file=self.JSON_FILEPATH, mode="r"):
            self.assertEqual(read_json(self.JSON_FILEPATH), self.DICT_DATA)
