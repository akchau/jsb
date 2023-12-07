import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IsNotListException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = [[1, "1", 12, 0, -1], []]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(
                BaseTypeManager().validate_list(data=value),
                value
            )


class TestWithBadCase(unittest.TestCase):

    def setUp(self):
        self.correct_values = [1.7, "1a", (1, 2, 3)]

    def test_with_invalide_values(self):
        for value in self.correct_values:
            with self.assertRaises(IsNotListException) as context:
                BaseTypeManager().validate_list(data=value)
                self.assertEqual(context.exception, f"{value} не список.")
