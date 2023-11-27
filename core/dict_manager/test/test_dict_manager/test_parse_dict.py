import unittest

from ...dict_manager import parse_dict


class TestParseDict(unittest.TestCase):
    """
    Тестирование функции validate_dict
    """

    def test_with_good_case(self):
        key1 = "key1"
        key2 = "key2"
        value = "value"
        TEST_DICT = {
            key1: {
                key2: value
            }
        }
        self.assertEqual(
            parse_dict(
                data=TEST_DICT,
                parse_keys=((key1, dict), (key2, str))
            ),
            value
        )
