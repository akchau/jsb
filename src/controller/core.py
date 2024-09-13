from src.controller.exc import NotAvailable
from src.services.api_client.api_client_types import StationsList, Station
from src.services.api_client.core import ApiInteractor
from src.services.db_client.core import RegisteredStationsDbClient


class ScheduleController:

    def __init__(self, api_interactor: ApiInteractor, entity: RegisteredStationsDbClient):
        self.__api_interactor = api_interactor
        self.__entity = entity

    # def get_schedule(self, arrived_station, departure_station):
    #     self.__api_client.get_schedule(arrived_station, departure_station)

    # def get_arrived_stations(self):
    #     self.__api_client.get_stations()

    async def get_available_for_registration_stations(self) -> StationsList:
        """
        Получение списка станций доступных для регистрации.
        """
        all_stations_of_base_branch: StationsList = await self.__api_interactor.list_available_stations()
        already_registered_stations_codes: list[str] = self.__entity.get_registered_stations_codes()
        return [station for station in all_stations_of_base_branch
                if station[1] not in already_registered_stations_codes]

    async def register_new_station(self, station_code: str) -> None:
        """
        Регистрация новой станции.
        """
        station: Station = await self.__api_interactor.get_station(station_code)
        if station is not None:
            self.__entity.register_station(station)
        else:
            raise NotAvailable("Такая станция недоступна.")

    async def get_registered_stations(self) -> StationsList:
        return self.__entity.get_registered_stations()
