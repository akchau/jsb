from . import controller_types, exc
from src.services.api_client.core import ApiInteractor
from src.services.db_client import RegisteredStationsDbClient, exc as db_exc


class ServiceInterface:

    def __init__(self, api: ApiInteractor, entity: RegisteredStationsDbClient):
        self.__api = api
        self.__entity = entity

    async def get_station_by_api(self, direction: controller_types.StationsDirection, code: str) -> controller_types.Station:
        all_stations_with_target_direction = await self.get_all_stations(direction)
        target_station: controller_types.Station = all_stations_with_target_direction.int_get_station_by_code(code)
        if target_station is not None:
            return target_station
        else:
            raise exc.NotAvailable("Такая станция недоступна.")

    async def get_all_stations(self, direction: controller_types.StationsDirection) -> controller_types.StationsList:
        list_stops_from_api: list[dict] = await self.__api.get_all_stations_for_base_stations_thread()
        return controller_types.StationsList(stations=[controller_types.Station(**stop, direction=direction) for stop in list_stops_from_api])

    async def get_all_registered_stations(self, direction: controller_types.StationsDirection) -> controller_types.StationsList:
        all_stations_from_db = await self.__entity.get_all_registered_stations(direction)
        return controller_types.StationsList(stations=[controller_types.Station(**stop) for stop in all_stations_from_db])


class ScheduleController:

    def __init__(self, api_interactor: ApiInteractor, entity: RegisteredStationsDbClient):
        self.service_interface = ServiceInterface(api_interactor, entity)
        self.__entity = entity

    async def get_registered_stations(self,
                                      direction: controller_types.StationsDirection) -> controller_types.ListStationInTuple:
        """
        Список станций зарегестированных в данном направлении.
        """
        all_registered_stations = await self.service_interface.get_all_registered_stations(direction)
        return all_registered_stations.ext_get_in_list_tuple()

    async def get_available_for_registration_stations_in_direction(self,
                                                                   direction: controller_types.StationsDirection) -> controller_types.ListStationInTuple:
        """
        Получение списка станций доступных для регистрации.
        """
        all_stations_with_target_direction: controller_types.StationsList = await self.service_interface.get_all_stations(direction)
        already_registered_stations_with_target_direction: controller_types.StationsList = await self.service_interface.get_all_registered_stations(direction)
        not_registered_stations_in_target_direction = all_stations_with_target_direction.int_get_not_in(
            already_registered_stations_with_target_direction
        )
        return not_registered_stations_in_target_direction.ext_get_in_list_tuple()

    async def register_new_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        """
        Регистрация новой станции.
        """
        try:
            new_station: controller_types.Station = await self.service_interface.get_station_by_api(direction, code)
            await self.__entity.register_station(new_station.dict())
        except db_exc.ExistException:
            pass

    async def delete_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        await self.__entity.delete_station(code, direction)

    async def move_station(self, direction: controller_types.StationsDirection, code: str) -> None:
        await self.__entity.move_station(code, direction)
