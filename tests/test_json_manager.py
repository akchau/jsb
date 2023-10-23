# import json
import json
import os
import shutil
import unittest

from core.json_manager import JsonManager
from core.json_manager import json_exceptions

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


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
        self.jm = JsonManager()

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

        self.assertTrue(self.jm.object_is_json_file(self.EXIST_JSON_FILEPATH))

    def test_with_not_json_file(self):
        """
        Тестируемая функция:

        - object_is_json_file()

        Тестируемое значение:

        - Путь текстового файла.
        """

        with open(self.EXIST_TXT_FILEPATH, 'w+'):
            pass

        self.assertFalse(self.jm.object_is_json_file(self.EXIST_TXT_FILEPATH))


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
    DICT_DATA = {"key": "value"}
    LIST_DATA = ["one", "two"]

    @classmethod
    def setUpClass(cls) -> None:
        cls.JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__JSON_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.jm = JsonManager()

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

        self.assertEqual(
            self.jm.read_json(self.JSON_FILEPATH),
            self.DICT_DATA
        )

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

        self.assertEqual(
            self.jm.read_json(self.JSON_FILEPATH),
            self.LIST_DATA
        )

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
        os.chmod(self.JSON_FILEPATH, 0o222)
        self.assertRaises(
            json_exceptions.NotPermissionForReadEntity,
            self.jm.read_json,
            self.JSON_FILEPATH
        )

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

        os.chmod(self.JSON_FILEPATH, 0o444)
        self.assertEqual(
            self.jm.read_json(self.JSON_FILEPATH),
            self.DICT_DATA
        )

    def test_with_empty_json(self):
        with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
            pass
        with self.assertRaises(json_exceptions.EmptyJsonEntity) as context:
            self.jm.read_json(filepath=self.JSON_FILEPATH)
        self.assertEqual(str(context.exception), "Открываемый json-файл пустой.")


class TestLoadDataInJson(unittest.TestCase):

    __JSON_FILENAME = "exist.json"
    __TEXT_FILENAME = "exist.txt"
    DICT_DATA = {"key": "value"}
    LIST_DATA = ["one", "two"]

    @classmethod
    def setUpClass(cls) -> None:
        cls.JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__JSON_FILENAME
        )
        cls.TEXT_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__TEXT_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.jm = JsonManager()

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_dict_with_exist_json_file(self):
        with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
            pass

        self.jm.load_data_in_json(
            filepath=self.JSON_FILEPATH,
            data=self.DICT_DATA
        )

        with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        self.assertEqual(
            data,
            self.DICT_DATA
        )

    def test_with_dict_with_not_exist_file(self):
        self.jm.load_data_in_json(
            filepath=self.JSON_FILEPATH,
            data=self.DICT_DATA
        )

        with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        self.assertEqual(
            data,
            self.DICT_DATA
        )

    def test_with_dict_with_exist_text_file(self):
        with open(file=self.TEXT_FILEPATH, mode="w", encoding='utf-8'):
            pass

        self.assertRaises(
            json_exceptions.AlreadyExistNotJsonEntity,
            self.jm.load_data_in_json,
            self.TEXT_FILEPATH,
            self.DICT_DATA
        )

    def test_with_list_with_exist_json_file(self):
        with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
            pass

        self.jm.load_data_in_json(
            filepath=self.JSON_FILEPATH,
            data=self.LIST_DATA
        )

        with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        self.assertEqual(
            data,
            self.LIST_DATA
        )
