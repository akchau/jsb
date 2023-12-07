import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IsNotIntException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = [1, "1", 12, 0, -1, "-10", "008", "-0010"]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(BaseTypeManager().validate_int(data=value), int(value))


class TestWithBadCase(unittest.TestCase):

    def setUp(self):
        self.incorrect_values = [1.7, "1a", [1, 2, 3], None]

    def test_with_invalide_values(self):
        for value in self.incorrect_values:
            with self.assertRaises(IsNotIntException) as context:
                BaseTypeManager().validate_int(data=value)
                self.assertEqual(context.exception, f"{value} не целое число.")
