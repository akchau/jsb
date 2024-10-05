"""
Главный модуль контроллера.
"""
from src.services.api_client.core import ApiInteractor
from .controller_types import StationActionEnum, StationsDirection, Station
from .exc import InternalError

from .managers.station_manger import StationManager
from ..services.db_client.core import ScheduleEntity


class ScheduleController:
    """
    Главный класс контоллера.
    """

    def __init__(self, api_interactor: ApiInteractor, entity: ScheduleEntity):
        self.admin_zone = StationManager(api_interactor, entity)

    async def change_station_callback(self, actual_condition):
        pass

    async def station_action(self, action: StationActionEnum, direction: str, code: str) -> None:

        actual_condition = None
        match action:
            case StationActionEnum.DELETE:
                actual_condition = await self.admin_zone.delete_station(direction, code)
            case StationActionEnum.MOVE:
                actual_condition = await self.admin_zone.move_station(direction, code)
            case StationActionEnum.REGISTER:
                actual_condition = await self.admin_zone.register_new_station(direction, code)
        if actual_condition:
            await self.change_station_callback(actual_condition)
        else:
            raise InternalError("Действие не вернуло актуальное сосотояние.")

    async def get_stations(self, direction: StationsDirection | None = None,
                           for_registration: bool = False, exclude_direction: bool = False) -> list[Station]:
        if for_registration and direction:
            return await self.admin_zone.get_available_for_registration_stations_in_direction(direction)
        elif direction is None:
            return await self.admin_zone.get_registered_stations()
        elif direction and exclude_direction is True:
            return await self.admin_zone.get_registered_stations(direction, exclude_direction)
        return await self.admin_zone.get_registered_stations(direction)