import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IsNotDictException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = [{1: "1", 12: 0, "one_key": "one"}, {}]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(
                BaseTypeManager().validate_dict(data=value),
                value
            )


class TestWithBadCase(unittest.TestCase):

    def setUp(self):
        self.incorrect_values = [1.7, "1a", (1, 2, 3)]

    def test_with_invalide_values(self):
        for value in self.incorrect_values:
            with self.assertRaises(IsNotDictException) as context:
                BaseTypeManager().validate_dict(data=value)
                self.assertEqual(context.exception, f"{value} не словарь.")
