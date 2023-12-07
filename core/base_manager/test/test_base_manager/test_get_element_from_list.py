import unittest
from ...base_manager import BaseTypeManager
from ...base_exceptions import IndexOutOfListException, IsNotListException, IsNotPositiveIntException


class TestWithGoodCase(unittest.TestCase):

    def setUp(self):
        self.data: list = [1, "1", 12, 0, "008"]
        self.list_index: int = 1

    def test_with_valide_values(self):
        self.assertEqual(
            BaseTypeManager().get_element_from_list(
                data=self.data,
                index=self.list_index
            ),
            self.data[self.list_index]
        )


class TestWithBadCase(unittest.TestCase):
    def setUp(self):
        self.data: list = [1, "1", 12, 0, "008"]
        self.not_list_data = (1, "1", 12, 0, "008")
        self.not_index = "not_index"
        self.list_index: int = len(self.data)

    def test_with_index_plus_one(self):
        with self.assertRaises(IndexOutOfListException) as context:
            BaseTypeManager().get_element_from_list(
                data=self.data,
                index=self.list_index
            )
            self.assertEqual(
                context.exception,
                (f"Значение {self.list_index} вышло за границы массива, "
                 f"который имеет длинну {len(self.data)}")
            )

    def test_with_not_list(self):
        """
        Тест случая, если в качестве списка передан не список.
        """
        with self.assertRaises(IsNotListException) as context:
            BaseTypeManager().get_element_from_list(
                data=self.not_list_data,
                index=self.list_index
            )
            self.assertEqual(
                context.exception,
                (f"{self.not_list_data} не список .")
            )

    def test_with_not_index(self):
        """
        Тест случая, если в качестве индекса передано не
        положительное целове число.
        """
        with self.assertRaises(IsNotPositiveIntException) as context:
            BaseTypeManager().get_element_from_list(
                data=self.not_list_data,
                index=self.not_index
            )
            self.assertEqual(
                context.exception,
                (f"{self.not_index} не целое положительное число.")
            )
