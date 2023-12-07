import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import NotValideTypeForKeyException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = [1, "one", ("one", 1)]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(
                BaseTypeManager().validate_dict_key(data=value),
                value
            )


class TestWithBadCase(unittest.TestCase):

    def setUp(self):
        self.incorrect_values = [{"one": "two"}, [1, 2, 3], None]

    def test_with_invalide_values(self):
        for value in self.incorrect_values:
            with self.assertRaises(NotValideTypeForKeyException) as context:
                BaseTypeManager().validate_dict_key(data=value)
                self.assertEqual(
                    context.exception,
                    f"{value} не целое положительное число."
                )
