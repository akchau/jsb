"""
Протестиированно:

- Метод DictValidator().clean_value

- Функция validate_dict()
"""

import unittest

from ...dict_manager import DictValidator, validate_dict
from ...dict_exceptions import IsNotDictException


class TestCleanValue(unittest.TestCase):
    """
    Тестирование метода clean_value
    """

    def test_with_invalide_data(self):
        """
        Тест со некорректными значениями.
        """

        test_values: list = [
            "test_string",
            5, None,
            "",
            ["one", "two"],
            ("one", "two")
        ]
        for test_value in test_values:
            with self.assertRaises(IsNotDictException) as context:
                DictValidator(data=test_value).clean_value
                self.assertEqual(
                    context.exception,
                    f"{test_value}\n--\nне слоарь. .")

    def test_with_correct_value(self):
        """
        Тест с корректными значениями.
        """
        test_values: list = [
            {},
            {
                "one": "two",
                "one": "two"
            }
        ]
        for test_value in test_values:
            self.assertEqual(
                DictValidator(data=test_value).clean_value,
                test_value
            )


class TestValidateDict(unittest.TestCase):
    """
    Тестирование функции validate_dict
    """

    def test_with_invalide_data(self):
        """
        Тест со некорректными значениями.
        """

        test_values: list = [
            "test_string",
            5, None,
            "",
            ["one", "two"],
            ("one", "two")
        ]
        for test_value in test_values:
            with self.assertRaises(IsNotDictException) as context:
                validate_dict(test_value)
                self.assertEqual(
                    context.exception,
                    f"{test_value}\n--\nне слоарь. .")

    def test_with_correct_value(self):
        """
        Тест с корректными значениями.
        """
        test_values: list = [
            {},
            {
                "one": "two",
                "one": "two"
            }
        ]
        for test_value in test_values:
            self.assertEqual(
                validate_dict(test_value),
                test_value
            )
