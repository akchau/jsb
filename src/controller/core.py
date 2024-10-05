"""
Главный модуль контроллера.
"""
from src.services.api_client.core import ApiInteractor
from .controller_types import StationActionEnum, StationsDirection, Station, DirectionType
from .exc import InternalError

from ..services.db_client.core import ScheduleEntity
from ..services.db_client.exc import ExistException


class ScheduleController:
    """
    Главный класс контоллера.
    """

    def __init__(self, api_interactor: ApiInteractor, entity: ScheduleEntity):
        self._entity = entity
        self._api = api_interactor

    async def change_station_callback(self, actual_condition):
        pass

    async def __get_registered_stations(self, direction: str = None,
                                      exclude_direction:bool = False) -> list[Station]:
        """
        Список станций зарегестированных в данном направлении.
        """
        clean_direction = DirectionType(direction=direction).direction \
            if direction is not None else None
        if direction is not None and exclude_direction:
            clean_direction = StationsDirection.FROM_MOSCOW \
                if clean_direction == StationsDirection.TO_MOSCOW else StationsDirection.TO_MOSCOW
        return await self._entity.get_all_registered_stations(clean_direction)

    async def station_action(self, action: str, direction: str, code: str) -> None:
        actual_condition = None
        clean_direction: StationsDirection = DirectionType(direction=direction).get_direction()
        match action:
            case StationActionEnum.DELETE:
                actual_condition = await self._entity.delete_station(code, clean_direction)
            case StationActionEnum.MOVE:
                actual_condition = await self._entity.move_station(code, clean_direction)
            case StationActionEnum.REGISTER:
                try:
                    list_stops_from_api: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
                    all_stations = [Station(**stop, direction=clean_direction) for stop in list_stops_from_api]
                    for available_station in all_stations:
                        if available_station.code == code:
                            actual_condition = await self._entity.register_station(available_station)
                except ExistException:
                    pass
        if actual_condition:
            await self.change_station_callback(actual_condition)
        else:
            raise InternalError("Действие не вернуло актуальное сосотояние.")

    async def get_stations(self, direction: str | None = None,
                           for_registration: bool = False, exclude_direction: bool = False) -> list[Station]:
        if for_registration and direction:
            list_stops_from_api: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
            all_stations = [Station(**stop, direction=DirectionType(direction=direction).get_direction()) for stop in list_stops_from_api]
            already_registered_stations: list[Station] = await self.__get_registered_stations(direction)
            return [station for station in all_stations if station not in already_registered_stations]
        elif direction is None:
            return await self.__get_registered_stations()
        elif direction and exclude_direction is True:
            return await self.__get_registered_stations(direction, exclude_direction)
        return await self.__get_registered_stations(direction)