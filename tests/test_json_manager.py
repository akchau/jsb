# import json
import json
import os
import shutil
import unittest

from core.json_manager.json_manager import JsonFileManager
from core.json_manager import json_exceptions

MODULE_PATH = os.path.abspath(__file__)
TEMP_FIXTURE_DIRPATH = os.path.join(
        os.path.dirname(MODULE_PATH),
        "__fixture__"
    )


class TestJsonFileManagerInit(unittest.TestCase):
    """
    Тестирование инициализации класса JsonFileManager
    """
    __JSON_FILENAME = "exist.json"
    __TEXT_FILENAME = "exist.txt"

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

    def test_init_with_json_filepath(self):
        jm = JsonFileManager(filepath=self.JSON_FILEPATH)
        self.assertEqual(jm.filepath, self.JSON_FILEPATH)

    def test_init_with_text_filepath(self):
        with self.assertRaises(json_exceptions.NotJsonPathEntity) as context:
            JsonFileManager(filepath=self.TEXT_FILEPATH)
            self.assertEqual(context.exception, (f"Путь {self.TEXT_FILEPATH} "
                                                 "является путем JSON-файла."))


class TestJsonFileExist(unittest.TestCase):
    """
    Тестирование функции _json_file_exist

    Тесты:

    - test_with_exist_json_file - Тестирование с путем
        существующего json-файла.

    - test_with_not_exist_json_file - Тестирование с путем несуществующего
        json-файла.
    """
    __EXIST_JSON_FILENAME = "exist.json"
    __NOT_EXIST_JSON_FILENAME = "not_exist.json"

    @classmethod
    def setUpClass(cls) -> None:
        cls.EXIST_JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__EXIST_JSON_FILENAME
        )
        cls.NOT_EXIST_JSON_FILEPATH = os.path.join(
            TEMP_FIXTURE_DIRPATH,
            cls.__NOT_EXIST_JSON_FILENAME
        )

    def setUp(self) -> None:
        """Создание папки для тестов __fixtures__."""
        os.mkdir(TEMP_FIXTURE_DIRPATH)
        self.jm_with_exist = JsonFileManager(self.EXIST_JSON_FILEPATH)
        self.jm_with_not_exist = JsonFileManager(self.NOT_EXIST_JSON_FILEPATH)
        with open(self.EXIST_JSON_FILEPATH, 'w+'):
            pass

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_exist_json_file(self):
        """
        Тестируемая функция:

        - _object_is_json_file()

        Тестируемое значение:

        - Путь json-файлa.
        """
        self.assertTrue(self.jm_with_exist._json_file_exist())

    def test_with_not_exist_json_file(self):
        """
        Тестируемая функция:

        - _object_is_json_file()

        Тестируемое значение:

        - Путь текстового файла.
        """
        self.assertFalse(self.jm_with_not_exist._json_file_exist())


class TestReadJson(unittest.TestCase):
    """
    Тестирование функции _read_json

    Тесты
    - test_with_dict - Тестирование с json-файлом в котором словарь.
    - test_with_list - Тестирование с json-файлом в котором список.
    - test_with_empty_json - Тестирование с пустым json-файлом.
    - test_with_not_exist_json - Тестирование с несуществующим json-файлом.
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
        self.jm = JsonFileManager(filepath=self.JSON_FILEPATH)

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
            self.jm._read_json(),
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
            self.jm._read_json(),
            self.LIST_DATA
        )

    def test_with_empty_json(self):
        with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
            pass
        with self.assertRaises(json_exceptions.EmptyJsonEntity) as context:
            self.jm._read_json()
            self.assertEqual(
                context.exception,
                (f"Json-файл {self.JSON_FILEPATH} "
                 "пустой, невозможно прочитать.")
            )

    def test_with_not_exist_json(self):
        with self.assertRaises(json_exceptions.NotExistEntity) as context:
            self.jm._read_json()
            self.assertEqual(
                context.exception,
                f"Файла {self.JSON_FILEPATH} не существует."
            )


class TestReadDictFromJson(unittest.TestCase):
    """
    Тестирование функции _read_dict_from_json

    Тесты
    - test_with_dict - Тестирование с json-файлом в котором словарь.
    - test_with_list - Тестирование с json-файлом в котором список.
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
        self.jm = JsonFileManager(
            filepath=self.JSON_FILEPATH)

    def tearDown(self) -> None:
        """Удаление папки для тестов __fixtures__."""
        shutil.rmtree(TEMP_FIXTURE_DIRPATH)

    def test_with_dict(self):
        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.DICT_DATA, new_json, indent=4, ensure_ascii=False)

        result = self.jm._read_dict_from_json()
        self.assertEqual(result, self.DICT_DATA)

    def test_with_list(self):
        with open(file=self.JSON_FILEPATH, mode="w",
                  encoding='utf-8') as new_json:
            json.dump(self.LIST_DATA, new_json, indent=4, ensure_ascii=False)

        with self.assertRaises(json_exceptions.DataIsNotDictEntity) as context:
            self.jm._read_dict_from_json()
            self.assertEqual(
                context.exception,
                f"Полученные или загружаемые данные {self.LIST_DATA} в/из "
                f"файл {self.JSON_FILEPATH}"
                f" имеют тип {type(self.LIST_DATA)} а не слоарь."
            )


# class TestLoadDataInJson(unittest.TestCase):

#     __JSON_FILENAME = "exist.json"
#     __TEXT_FILENAME = "exist.txt"
#     DICT_DATA = {"key": "value"}
#     LIST_DATA = ["one", "two"]

#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.JSON_FILEPATH = os.path.join(
#             TEMP_FIXTURE_DIRPATH,
#             cls.__JSON_FILENAME
#         )
#         cls.TEXT_FILEPATH = os.path.join(
#             TEMP_FIXTURE_DIRPATH,
#             cls.__TEXT_FILENAME
#         )

#     def setUp(self) -> None:
#         """Создание папки для тестов __fixtures__."""
#         os.mkdir(TEMP_FIXTURE_DIRPATH)
#         self.jm = JsonFileManager(filepath=self.JSON_FILEPATH)

#     def tearDown(self) -> None:
#         """Удаление папки для тестов __fixtures__."""
#         shutil.rmtree(TEMP_FIXTURE_DIRPATH)

#     def test_with_dict_with_exist_json_file(self):
#         with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
#             pass

#         self.jm._load_data_in_json(
#             data=self.DICT_DATA
#         )

#         with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
#             data = json.load(json_file)

#         self.assertEqual(
#             data,
#             self.DICT_DATA
#         )

#     def test_with_dict_with_not_exist_file(self):
#         self.jm._load_data_in_json(
#             data=self.DICT_DATA
#         )

#         with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
#             data = json.load(json_file)

#         self.assertEqual(
#             data,
#             self.DICT_DATA
#         )

#     def test_with_dict_with_exist_text_file(self):
#         with open(file=self.TEXT_FILEPATH, mode="w", encoding='utf-8'):
#             pass

#         self.assertRaises(
#             json_exceptions.AlreadyExistNotJsonEntity,
#             self.jm._load_data_in_json,
#             self.TEXT_FILEPATH,
#             self.DICT_DATA
#         )

#     def test_with_list_with_exist_json_file(self):
#         with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
#             pass

#         self.jm._load_data_in_json(
#             filepath=self.JSON_FILEPATH,
#             data=self.LIST_DATA
#         )

#         with open(file=self.JSON_FILEPATH, mode='r', encoding='utf-8') as json_file:
#             data = json.load(json_file)

#         self.assertEqual(
#             data,
#             self.LIST_DATA
#         )

#     def test_without_write_permission(self):
#         with open(file=self.JSON_FILEPATH, mode="w", encoding='utf-8'):
#             pass
#         os.chmod(self.JSON_FILEPATH, 0o444)
#         with self.assertRaises(json_exceptions.NotPermissionForWriteEntity) as context:
#             self.jm._load_data_in_json(
#                 filepath=self.JSON_FILEPATH,
#                 data=self.LIST_DATA
#             )
#             self.assertEqual(
#                 str(context.exception),
#                 "Недостаточно прав на запись в json-файл."
#             )


# class TestReadDictRecordFromJson(unittest.TestCase):

#     __JSON_FILENAME = "exist.json"
#     EXIST_KEY_1_LVL = "exits_key_1"
#     EXIST_KEY_2_LVL = "exits_key_2"
#     EXIST_VALUE = "value_1"
#     NOT_EXIST_KEY = "exits_key_3"
#     TEST_DATA = {
#         EXIST_KEY_1_LVL: {
#             EXIST_KEY_2_LVL: EXIST_VALUE
#         }
#     }

#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.JSON_FILEPATH = os.path.join(
#             TEMP_FIXTURE_DIRPATH,
#             cls.__JSON_FILENAME
#         )

#     def setUp(self) -> None:
#         """Создание папки для тестов __fixtures__."""
#         os.mkdir(TEMP_FIXTURE_DIRPATH)
#         self.jm = JsonManager()
#         with open(file=self.JSON_FILEPATH, mode="w") as json_file:
#             json.dump(self.TEST_DATA, json_file, indent=4, ensure_ascii=False)

#     def tearDown(self) -> None:
#         """Удаление папки для тестов __fixtures__."""
#         shutil.rmtree(TEMP_FIXTURE_DIRPATH)

#     def test_with_exist_key(self):
#         value = self.jm.read_dict_record_from_json(
#             filepath=self.JSON_FILEPATH,
#             keys=(self.EXIST_KEY_1_LVL, self.EXIST_KEY_2_LVL)
#         )
#         self.assertEqual(value, self.EXIST_VALUE)

#     def test_with_not_exist_key(self):
#         with self.assertRaises(json_exceptions.KeyNotExistInJsonDict) as context:
#             self.jm.read_dict_record_from_json(
#                 filepath=self.JSON_FILEPATH,
#                 keys=(self.EXIST_KEY_1_LVL, self.NOT_EXIST_KEY)
#             )
#             self.assertEqual(
#                 context.exception,
#                 (f"В файле {self.JSON_FILEPATH} не существует "
#                  "ключа {self.NOT_EXIST_KEY}.")
#             )
