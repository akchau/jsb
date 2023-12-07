import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import KeyNotExistInDict, IsNotDictException, NotValideTypeForKeyException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.data: list = {"one": "1", "two": "2"}
        self.dict_key: int = "one"

    def test_with_valide_values(self):
        self.assertEqual(
            BaseTypeManager().get_element_from_dict(
                data=self.data,
                dict_key=self.dict_key
            ),
            self.data[self.dict_key]
        )


class TestWithBadCase(unittest.TestCase):
    def setUp(self):
        self.data: list = {"one": "1", "two": "2"}
        self.dict_key: int = "one"
        self.not_exist_dict_key: int = "three"
        self.not_key = ["not_index"]
        self.not_dict_data: int = ["one", "two", "three"]

    def test_not_exist_key(self):
        with self.assertRaises(KeyNotExistInDict) as context:
            BaseTypeManager().get_element_from_dict(
                data=self.data,
                dict_key=self.not_exist_dict_key
            )
            self.assertEqual(
                context.exception,
                f"Ключа {self.not_exist_dict_key} нет в словаре\n{self.data}."
            )

    def test_with_not_dict(self):
        """
        Тест случая, если в качестве словаря передан не словарь.
        """
        with self.assertRaises(IsNotDictException) as context:
            BaseTypeManager().get_element_from_dict(
                data=self.not_dict_data,
                dict_key=self.dict_key
            )
            self.assertEqual(
                context.exception,
                (f"{self.not_dict_data} не словарь.")
            )

    def test_with_not_index(self):
        """
        Тест случая, если в качестве ключа передан тип дпнных
        который не может быть ключом.
        """
        with self.assertRaises(NotValideTypeForKeyException) as context:
            BaseTypeManager().get_element_from_dict(
                data=self.data,
                dict_key=self.not_key
            )
            self.assertEqual(
                context.exception,
                (f"Значение {self.not_key} имеет тип {type(self.not_key)} и"
                 " не может быть ключом словаря.")
            )
