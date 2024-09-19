import unittest
from unittest.mock import Mock

from src.controller.controller_types import StationsDirection
from src.services.db_client import RegisteredStationsDbClient
from . import conftest


TEST_DB_HOST = "host"
TEST_DB_PORT = 80
TEST_DB_USER = "username"
TEST_DB_PASSWORD = "password"


class TestGetAllRegisteredStations(unittest.IsolatedAsyncioTestCase):
    """
    Тестирование функции - Получить все зарегестрированные станции.
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
        Транспорт вернул список.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"direction": StationsDirection.FROM_MOSCOW, "id": "one"},
                {"direction": StationsDirection.FROM_MOSCOW, "id": "two"},
                {"direction": StationsDirection.TO_MOSCOW, "id": "three"},
            ]
        ]
        result = await self.client.get_all_registered_stations(direction=StationsDirection.FROM_MOSCOW)
        self.assertEqual(
            result,
            [
                {"direction": StationsDirection.FROM_MOSCOW, "id": "one"},
                {"direction": StationsDirection.FROM_MOSCOW, "id": "two"},
            ]
        )

    async def test_good_case_empty(self):
        """
        Транспорт ничего не вернул.
        """
        self.mock_transport.get_list.side_effect = [[]]
        result = await self.client.get_all_registered_stations(direction=StationsDirection.FROM_MOSCOW)
        self.assertEqual(result, [])

    async def test_good_case_not_target(self):
        """
        Транспорт вернул список без целевого направления.
        """
        self.mock_transport.get_list.side_effect = [
            [
                {"direction": StationsDirection.FROM_MOSCOW, "id": "one"},
                {"direction": StationsDirection.FROM_MOSCOW, "id": "two"},
                {"direction": StationsDirection.FROM_MOSCOW, "id": "three"},
            ]
        ]
        result = await self.client.get_all_registered_stations(direction=StationsDirection.TO_MOSCOW)
        self.assertEqual(result, [])
