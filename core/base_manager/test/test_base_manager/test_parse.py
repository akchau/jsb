import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IsNotIntException, IsNotPositiveIntException


class TestWithGoodCaseParseList(unittest.TestCase):

    def setUp(self):
        self.data: list = [1, "1", 12, 0, "008"]
        self.list_index: int = 1

    def test_with_valide_values(self):
        self.assertEqual(
            BaseTypeManager().parse(data=self.data, keys=[(self.list_index, list)]),
            self.data[self.list_index]
        )


class TestWithGoodCaseParseDict(unittest.TestCase):

    def setUp(self):
        self.data: list = {1: "1", 12: 0, "eight": "008"}
        self.list_index: int = 1

    def test_with_valide_values(self):
        self.assertEqual(
            BaseTypeManager().parse(data=self.data, keys=[(self.list_index, dict)]),
            self.data[self.list_index]
        )


class TestWithGoodCaseParseComplexStruxure(unittest.TestCase):

    def setUp(self):
        self.one_index: str = "one_object"
        self.two_index: str = "list_object"
        self.list_index: int = 1
        self.value: int = 10
        self.data: list = {self.one_index: {self.two_index: [12, self.value, 13]}}

    def test_with_valide_values(self):
        self.assertEqual(
            BaseTypeManager().parse(
                data=self.data,
                keys=[(self.one_index, dict), (self.two_index, dict), (self.list_index, list)]
            ),
           self.value
        )