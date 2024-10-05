from src.controller import controller_types

from src.services.api_client import ApiInteractor
from src.services.db_client import ScheduleEntity


class BaseManager:

    def __init__(self, api_interactor: ApiInteractor, entity: ScheduleEntity):
        self._api = api_interactor
        self._entity = entity

    async def get_registered_stations(self, direction: str = None,
                                      exclude_direction:bool = False) -> list[controller_types.Station]:
        """
        Список станций зарегестированных в данном направлении.
        """
        clean_direction = controller_types.DirectionType(direction=direction).direction \
            if direction is not None else None
        if direction is not None and exclude_direction:
            clean_direction = controller_types.StationsDirection.FROM_MOSCOW \
                if clean_direction == controller_types.StationsDirection.TO_MOSCOW else (
                controller_types.StationsDirection.TO_MOSCOW)
        return await self._entity.get_all_registered_stations(clean_direction)
