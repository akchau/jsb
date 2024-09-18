from pydantic import ValidationError
from api_client import ApiClient, RequestException

from src.services.api_client.api_client_types import ScheduleFromBaseStation, ThreadData
from src.services.api_client.exc import ApiError


class TransportApiClient(ApiClient):

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
        print(result)
        return ScheduleFromBaseStation.parse_obj(result)

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
        return ThreadData.parse_obj(all_stations_data)


class ApiInteractor:
    """
    Интерактор для работы с API.
    """
    def __init__(self, api_client: TransportApiClient):
        self.__api_client = api_client

    async def get_all_stations_for_base_stations_thread(self) -> list[dict]:
        """
        Получение списка станций или станции по коду.
        """
        try:

            branch = await self.__api_client.get_branch_info()
            thread = await self.__api_client.get_thread_info(branch.get_thread_uid())
            return thread.ext_get_stations()
        except RequestException as e:
            raise ApiError(str(e))
        except ValidationError as e:
            raise ApiError(f"Ошибка валидации ответа API {str(e)}")
