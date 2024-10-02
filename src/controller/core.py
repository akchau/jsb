"""
Главный модуль контроллера.
"""
from src.services.api_client.core import ApiInteractor
from .controller_types import DirectionType, StationsDirection
from ..services.db_client.core import ScheduleEntity
from ..services.db_client.exc import ExistException
from . import controller_types


class ScheduleController:
    """
    Главный класс контоллера.
    """

    def __init__(self, api_interactor: ApiInteractor, entity: ScheduleEntity):
        self.__api = api_interactor
        self.__entity = entity
        self.__entity.set_on_station_change(self.on_change_station_callback)

    async def __get_all_available_stations(self, direction: StationsDirection) -> list[controller_types.Station]:
        """
        Получение доступных для регистрации станции.
        :param direction:
        :return:
        """
        list_stops_from_api: list[dict] = await self.__api.get_all_stations_for_base_stations_thread()
        return [controller_types.Station(**stop, direction=direction) for stop in list_stops_from_api]

    async def on_change_station_callback(self, current_stations):
        """
        Колебек вызываемый при изменении состава зарегистрированных станции.
        :return:
        """
        print(current_stations)

    async def get_registered_stations(self, direction: str) -> list[controller_types.Station]:
        """
        Список станций зарегестированных в данном направлении.
        """
        clean_direction = DirectionType(direction=direction).direction
        return await self.__entity.get_all_registered_stations(clean_direction)

    async def get_available_for_registration_stations_in_direction(self,
                                                                   direction: controller_types.StationsDirection
                                                                   ) -> list[controller_types.Station]:
        """
        Получение списка станций доступных для регистрации.
        """
        all_stations: list[controller_types.Station] = await self.__get_all_available_stations(direction)
        already_registered_stations: list[controller_types.Station] = await self.get_registered_stations(direction)
        return [station for station in all_stations if station not in already_registered_stations]

    async def register_new_station(self, direction: str, code: str) -> None:
        """
        Регистрация новой станции.
        """

        clean_direction = DirectionType(direction=direction)
        try:
            all_stations: list[controller_types.Station] = await self.__get_all_available_stations(
                clean_direction.get_direction()
            )
            for available_station in all_stations:
                if available_station.code == code:
                    await self.__entity.register_station(available_station)
        except ExistException:
            pass

    async def delete_station(self, direction: str, code: str) -> None:
        """
        Удаление станции.
        :param direction: Направление удаляемой станции.
        :param code: Код станции.
        :return:
        """
        clean_direction = DirectionType(direction=direction).direction
        await self.__entity.delete_station(code, clean_direction)

    async def move_station(self, direction: str, code: str) -> None:
        """
        Перемещение станции.
        :param direction: Направление перемещаемой станции.
        :param code: Код перемещаемой станции.
        :return:
        """
        clean_direction = DirectionType(direction=direction).direction
        await self.__entity.move_station(code, clean_direction)

    # async def refresh_schedules(self, depart):
    #     register_stations = self.service_interface.get_all_registered_stations()
