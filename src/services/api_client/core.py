"""
Api-клиент
"""
import datetime
from api_client import ApiClient

from src.services.api_client.api_client_types import ScheduleFromBaseStation, ThreadData, StoreType, \
    ScheduleResponse


class TransportApiClient(ApiClient):
    """
    Клиент api Yandex-транспортa.
    """
    store: StoreType
    _schedule_from_base_station_model = ScheduleFromBaseStation
    _thread_data_model = ThreadData

    async def get_branch_info(self) -> ScheduleFromBaseStation:
        """
        Запрос, кода ветки базовой станции.
        """
        result = self.transport.get(
            path="schedule/",
            headers={"Content-Type": "application/json"},
            params={
                "apikey": self.store.api_key,
                "station": self.store.base_station_code,
                "transport_types": "suburban"
            }
        )
        return self._schedule_from_base_station_model.parse_obj(result)

    async def get_thread_info(self, thread_uid: str) -> ThreadData:
        """
        Запрос, станций из ветки.
        """
        all_stations_data = self.transport.get(
            path="thread/",
            headers={"Content-Type": "application/json"},
            params={
                "apikey": self.store.api_key,
                "uid": thread_uid
            }
        )
        return self._thread_data_model.parse_obj(all_stations_data)

    async def get_schedule(self, departure_station_code: str, arrived_station_code: str):
        schedule = self.transport.get(
            path="search/",
            params={
                "apikey": self.store.api_key,
                "from": departure_station_code,
                "to": arrived_station_code,
                "date": datetime.datetime.today()
            }
        )
        return ScheduleResponse.parse_obj(schedule)
