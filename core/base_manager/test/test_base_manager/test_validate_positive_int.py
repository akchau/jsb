import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IsNotIntException, IsNotPositiveIntException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = [1, "1", 12, 0, "008"]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(
                BaseTypeManager().validate_positive_int(data=value),
                int(value)
            )


class TestWithBadCase(unittest.TestCase):

    def setUp(self):
        self.correct_values = [-1, 1.7, "1a", [1, 2, 3], "-1", "-0010"]

    def test_with_invalide_values(self):
        for value in self.correct_values:
            with self.assertRaises(IsNotPositiveIntException) as context:
                BaseTypeManager().validate_positive_int(data=value)
                self.assertEqual(
                    context.exception,
                    f"{value} не целое положительное число."
                )
