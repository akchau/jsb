import unittest
from unittest.mock import Mock

from src.controller.controller_types import StationsDirection
from src.services.db_client import RegisteredStationsDbClient
from src.services.db_client.exc import NotExistException, DbClientException

TEST_DB_NAME = "db_name"
TEST_DB_HOST = "host"
TEST_DB_PORT = 80
TEST_DB_USER = "username"
TEST_DB_PASSWORD = "password"
TEST_CODE = "test"
TEST_RECORD_ID_ONE = "test_id_one"
TEST_RECORD_ID_TWO = "test_id_two"


class TestDeleteStation(unittest.IsolatedAsyncioTestCase):
    """
    Тестирование функции - Удалить запись.
    """
    def setUp(self):
        mock_transport_class = Mock()
        self.mock_transport = Mock()
        mock_transport_class.return_value = self.mock_transport
        self.client = RegisteredStationsDbClient(
            db_name=TEST_DB_NAME,
            db_host=TEST_DB_HOST,
            db_user=TEST_DB_USER,
            db_password=TEST_DB_PASSWORD,
            dp_port=TEST_DB_PORT,
            _transport_class=mock_transport_class
        )

    async def test_good_case(self):
        """
        Успешное удаление станции.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW},
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ],
            [
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        result = await self.client.delete_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.assertEqual(
            result,
            {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW})
        self.mock_transport.delete.assert_called_with(
            collection_name="stations",
            instance_id=TEST_RECORD_ID_ONE
        )

    async def test_bad_case_not_exist(self):
        """
        Удаляемый объект не существует.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ],
            []
        ]
        with self.assertRaises(NotExistException):
            await self.client.delete_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.mock_transport.delete.assert_not_called()

    async def test_bad_case_not_delete(self):
        """
        Объект не удалился.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW},
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ],
            [
                {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW},
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        with self.assertRaises(DbClientException):
            await self.client.delete_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.mock_transport.delete.assert_called_with(
            collection_name="stations",
            instance_id=TEST_RECORD_ID_ONE
        )


