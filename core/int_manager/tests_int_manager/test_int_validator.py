"""
Протестиированно:

- Метод IntValidator().clean_value

- Функция validate_int()
"""

import unittest

from ..int_manager import validate_int, IntValidator
from ..int_exceptoins import IsNotIntException


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
            None,
            "",
            ["one", "two"],
            ("one", "two")
        ]
        for test_value in test_values:
            with self.assertRaises(IsNotIntException) as context:
                IntValidator(data=test_value).clean_value
                self.assertEqual(
                    context.exception,
                    f"{test_value} не целое .")

    def test_with_correct_value(self):
        """
        Тест с корректными значениями.
        """
        test_values: list = [
            5
        ]
        for test_value in test_values:
            self.assertEqual(
                IntValidator(data=test_value).clean_value,
                test_value
            )


class TestValidateInt(unittest.TestCase):
    """
    Тестирование функции validate_int
    """

    def test_with_invalide_data(self):
        """
        Тест со некорректными значениями.
        """

        test_values: list = [
            "test_string",
            None,
            "",
            ["one", "two"],
            ("one", "two")
        ]
        for test_value in test_values:
            with self.assertRaises(IsNotIntException) as context:
                validate_int(data=test_value)
                self.assertEqual(
                    context.exception,
                    f"{test_value} не целое .")

    def test_with_correct_value(self):
        """
        Тест с корректными значениями.
        """
        test_values: list = [
            5
        ]
        for test_value in test_values:
            self.assertEqual(
                validate_int(test_value),
                test_value
            )
