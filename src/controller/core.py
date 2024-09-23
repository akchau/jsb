from pydantic import ValidationError

from . import controller_types, exc
from src.services.api_client.core import ApiInteractor
from src.services.db_client import RegisteredStationsDbClient, exc as db_exc
from .controller_types import Station
from .exc import InternalError
from ..services.db_client.core import ScheduleDbCollection


class ScheduleController:

    def __init__(self, api_interactor: ApiInteractor, stations_entity: RegisteredStationsDbClient,
                 schedule_entity: ScheduleDbCollection):
        self.__api = api_interactor
        self.__entity = stations_entity
        self.__schedule_entity = schedule_entity

    async def __get_all_available_stations(self, direction) -> list[Station]:
        list_stops_from_api: list[dict] = await self.__api.get_all_stations_for_base_stations_thread()
        return [controller_types.Station(**stop, direction=direction) for stop in list_stops_from_api]

    async def get_registered_stations(self, direction: controller_types.StationsDirection) -> list[Station]:
        """
        Список станций зарегестированных в данном направлении.
        """
        try:
            return [
                Station(**station.dict())
                for station in await self.__entity.get_all_registered_stations(direction=direction)
            ]
        except ValidationError:
            raise InternalError("Данные получены в неверном формате")

    async def get_available_for_registration_stations_in_direction(self,
                                                                   direction: controller_types.StationsDirection
                                                                   ) -> list[Station]:
        """
        Получение списка станций доступных для регистрации.
        """
        all_stations: list[Station] = await self.__get_all_available_stations(direction)
        already_registered_stations: list[Station] = await self.get_registered_stations(direction)
        return [station for station in all_stations if station not in already_registered_stations]

    async def register_new_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        """
        Регистрация новой станции.
        """
        try:
            all_stations: list[Station] = await self.__get_all_available_stations(direction)
            for available_station in all_stations:
                if available_station.code == code:
                    await self.__entity.register_station(available_station)
        except db_exc.ExistException:
            pass

    async def delete_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        await self.__entity.delete_station(code, direction)

    async def move_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        await self.__entity.move_station(code, direction)

    # async def refresh_schedules(self, depart):
    #     register_stations = self.service_interface.get_all_registered_stations()