from pydantic import ValidationError

from api_client import ApiClient, RequestException

from src.services.api_client.api_client_types import ScheduleFromBaseStation, StationsOfThread, StationsList, Station
from src.services.api_client.exc import ApiError


class TransportApiClient(ApiClient):

    CONTENT_TYPE = {"Content-Type": "application/json"}

    async def get_branch_uid(self) -> str:
        """
        Запрос, кода ветки базовой станции.
        """
        result = self.transport.get(
            path="schedule/",
            headers=self.CONTENT_TYPE,
            params={
                "apikey": self.store["api_key"],
                "station": self.store["base_station_code"],
                "transport_types": "suburban"
            }
        )
        return ScheduleFromBaseStation.parse_obj(result).get_thread_uid()

    async def get_stations_of_thread(self, thread_uid) -> StationsList:
        """
        Запрос, станций из ветки.
        """
        all_stations_data = self.transport.get(
            path="thread/",
            headers=self.CONTENT_TYPE,
            params={
                "apikey": self.store["api_key"],
                "uid": thread_uid
            }
        )
        return StationsOfThread.parse_obj(all_stations_data).get_stations()


class ApiInteractor:
    """
    Интерактор для работы с API.
    """
    def __init__(self, api_client: TransportApiClient):
        self.__api_client = api_client

    async def list_available_stations(self) -> StationsList:
        """
        Получение списка станций или станции по коду.
        """
        try:
            thread_uid = await self.__api_client.get_branch_uid()
            return await self.__api_client.get_stations_of_thread(thread_uid)
        except RequestException as e:
            raise ApiError(str(e))
        except ValidationError:
            raise ApiError("Ошибка валидации ответа API")

    async def get_station(self, code: str) -> Station | None:
        """
        Получение станции по коду.
        """
        all_stations: StationsList = await self.list_available_stations()
        find_station = [station for station in all_stations if station[1] == code]
        if len(find_station) == 0:
            return None
        return find_station[0]
