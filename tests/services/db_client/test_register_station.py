import unittest
from unittest.mock import Mock

from src.controller.controller_types import StationsDirection
from src.services.db_client import RegisteredStationsDbClient
from src.services.db_client.exc import ExistException, DbClientException

TEST_DB_NAME = "db_name"
TEST_DB_HOST = "host"
TEST_DB_PORT = 80
TEST_DB_USER = "username"
TEST_DB_PASSWORD = "password"


class TestRegisterStation(unittest.IsolatedAsyncioTestCase):
    """
    Тестирование функции - Зарегистрировать станциию.
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
        Запись создалась.
        """

        self.mock_transport.get_list.side_effect = [
            [
                {"code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ],
            [
                {"code": "one", "direction": StationsDirection.FROM_MOSCOW},
                {"code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        result = await self.client.register_station(station={"code": "one", "direction": StationsDirection.FROM_MOSCOW})
        self.assertEqual(result, {"code": "one", "direction": StationsDirection.FROM_MOSCOW})
        self.mock_transport.post.assert_called_with(
            "stations",
            {"code": "one", "direction": StationsDirection.FROM_MOSCOW}
        )

    async def test_already_exist(self):
        """
        Такая запись уже существует.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"code": "one", "direction": StationsDirection.FROM_MOSCOW},
                {"code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        with self.assertRaises(ExistException):
            await self.client.register_station(station={"code": "one", "direction": StationsDirection.FROM_MOSCOW})
        self.mock_transport.post.assert_not_called()

    async def test_not_create(self):
        """
        Запись не создалась.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ],
            [
                {"code": "two", "direction": StationsDirection.FROM_MOSCOW}
            ]
        ]
        with self.assertRaises(DbClientException):
            await self.client.register_station(station={"code": "one", "direction": StationsDirection.FROM_MOSCOW})
        self.mock_transport.post.assert_called_with(
            "stations",
            {"code": "one", "direction": StationsDirection.FROM_MOSCOW}
        )

