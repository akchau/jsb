import unittest
from ...base_manager import BaseTypeManager


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.correct_values: list = ["path", "/path", "/path/", "path/", " /path", " /path/ "]

    def test_with_valide_values(self):
        for value in self.correct_values:
            self.assertEqual(
                BaseTypeManager().slice_path(value=value),
                "path"
            )
