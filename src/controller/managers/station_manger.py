from src.controller import controller_types
from src.controller.controller_types import StationsDirection, DirectionType
from src.controller.managers.base import BaseManager
from src.services.db_client.exc import ExistException


class StationManager(BaseManager):

    async def __get_all_available_stations(self, direction: StationsDirection) -> list[controller_types.Station]:
        """
        Получение доступных для регистрации станции.
        :param direction:
        :return:
        """
        list_stops_from_api: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
        return [controller_types.Station(**stop, direction=direction) for stop in list_stops_from_api]

    async def get_available_for_registration_stations_in_direction(self,
                                                                   direction: controller_types.StationsDirection
                                                                   ) -> list[controller_types.Station]:
        """
        Получение списка станций доступных для регистрации.
        """
        all_stations: list[controller_types.Station] = await self.__get_all_available_stations(direction)
        already_registered_stations: list[controller_types.Station] = await self.get_registered_stations(direction)
        return [station for station in all_stations if station not in already_registered_stations]

    async def register_new_station(self, direction: str, code: str):
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
                    return await self._entity.register_station(available_station)
        except ExistException:
            pass

    async def delete_station(self, direction: str, code: str):
        """
        Удаление станции.
        :param direction: Направление удаляемой станции.
        :param code: Код станции.
        :return:
        """
        clean_direction = DirectionType(direction=direction).direction
        return await self._entity.delete_station(code, clean_direction)

    async def move_station(self, direction: str, code: str):
        """
        Перемещение станции.
        :param direction: Направление перемещаемой станции.
        :param code: Код перемещаемой станции.
        :return:
        """
        clean_direction = DirectionType(direction=direction).direction
        return await self._entity.move_station(code, clean_direction)