"""
Api-клиент
"""
import datetime

from pydantic import ValidationError
from api_client import ApiClient, RequestException

from src.services.api_client.api_client_types import ScheduleFromBaseStation, ThreadData, StoreType, ScheduleModel
from src.services.api_client.exc import ParsingApiResponseError, InternalApiError


class TransportApiClient(ApiClient):
    """
    Клиент api Yandex-транспортa.
    """

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
        return ScheduleModel.parse_obj(schedule)


class ApiInteractor:
    """
    Интерактор для работы с API.
    """
    def __init__(self, base_url: str, api_key: str, base_station_code: str):
        self._store_type = StoreType
        self.__api_client = TransportApiClient(base_url=base_url, api_prefix="v3.0", store=self._store_type(
            api_key=api_key, base_station_code=base_station_code
        ))
        self._internal_api_error = InternalApiError
        self._parsing_api_error = ParsingApiResponseError

    async def get_schedule(self, departure_station_code, arrived_station_code):
        try:
            direct = await self.__api_client.get_schedule(departure_station_code, arrived_station_code)
            back = await self.__api_client.get_schedule(arrived_station_code, departure_station_code)
            return direct.ext(), back.ext()
        except RequestException as e:
            raise self._internal_api_error(str(e))
        except ValidationError as e:
            raise self._parsing_api_error(f"Ошибка валидации ответа API {str(e)}")

    async def get_all_stations_for_base_stations_thread(self) -> list[dict]:
        """
        Получение списка станций или станции по коду.
        """
        try:

            branch = await self.__api_client.get_branch_info()
            thread = await self.__api_client.get_thread_info(branch.get_thread_uid())
            return thread.ext_get_stations()
        # TODO тут иногда при плохом соединений слетает, нужен презапуск встроенный или внешний
        except RequestException as e:
            raise self._internal_api_error(str(e))
        except ValidationError as e:
            raise self._parsing_api_error(f"Ошибка валидации ответа API {str(e)}")
