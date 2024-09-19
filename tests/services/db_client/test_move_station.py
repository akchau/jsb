import unittest
from unittest.mock import Mock

from src.controller.controller_types import StationsDirection
from src.services.db_client import RegisteredStationsDbClient
from src.services.db_client.exc import NotExistException, DbClientException
from . import conftest


TEST_DB_HOST = "host"
TEST_DB_PORT = 80
TEST_DB_USER = "username"
TEST_DB_PASSWORD = "password"
TEST_CODE = "test"
TEST_RECORD_ID_ONE = "test_id_one"
TEST_RECORD_ID_TWO = "test_id_two"


class TestMoveStation(unittest.IsolatedAsyncioTestCase):
    """
    Тестирование функции - Сменить направление станции.
    """

    def setUp(self):
        mock_transport_class = Mock()
        self.mock_transport = Mock()
        mock_transport_class.return_value = self.mock_transport
        self.client = RegisteredStationsDbClient(
            db_name=conftest.TEST_DB_NAME,
            db_host=TEST_DB_HOST,
            db_user=TEST_DB_USER,
            db_password=TEST_DB_PASSWORD,
            dp_port=TEST_DB_PORT,
            _transport_class=mock_transport_class
        )

    async def test_good_case(self):
        """
        Смена направления успешна.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW},
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        self.mock_transport.get.side_effect = [
            {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.TO_MOSCOW}
        ]
        await self.client.move_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.mock_transport.update_field.assert_called_with(
            collection_name="stations",
            field_name="direction",
            new_value=StationsDirection.TO_MOSCOW,
            instance_id=TEST_RECORD_ID_ONE
        )

    async def test_bad_case_not_exist(self):
        """
        Станция не существует.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        self.mock_transport.get.side_effect = []
        with self.assertRaises(NotExistException):
            await self.client.move_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.mock_transport.update_field.assert_not_called()

    async def test_not_update(self):
        """
        Станция не обновилась.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW},
                {"_id": TEST_RECORD_ID_TWO, "code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        self.mock_transport.get.side_effect = [
            {"_id": TEST_RECORD_ID_ONE, "code": TEST_CODE, "direction": StationsDirection.FROM_MOSCOW}
        ]
        with self.assertRaises(DbClientException):
            await self.client.move_station(TEST_CODE, StationsDirection.FROM_MOSCOW)
        self.mock_transport.update_field.assert_called_with(
            collection_name="stations",
            field_name="direction",
            new_value=StationsDirection.TO_MOSCOW,
            instance_id=TEST_RECORD_ID_ONE
        )
