from typing import Type

from src.domain.base import BaseApp
from src.domain.controller_types import DirectionType, StationsDirection, StationActionEnum, SchedulesBetweenStations
from src.domain.exc import InternalError
from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity, DbClientException
from src.services.db_client.db_client_types import StationDocumentModel, ScheduleDocumentModel


def base_error_handler(func):

    """
    Декоратор обработает ошибки при работе с api
    Глобальная ошибка которую выбрасывает транспорт -> Внутренняя ошибка.
    Ошибка при парсинге модели ответа -> Внутренняя ошибка.
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DbClientException as e:
            raise InternalError(str(e))
    return wrapper


class AdminApp(BaseApp):

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        super().__init__(view, entity)

        self._internal_error = InternalError
        self._direction_validator = DirectionType
        self._station_direction = StationsDirection
        self._action_enum = StationActionEnum


    async def __call_change_station_callback(self, actual_stations_list: list[StationDocumentModel]):
        registered_stations_from_moscow: list[StationDocumentModel] = [
            station for station in actual_stations_list if station.direction == self._station_direction.FROM_MOSCOW
        ]
        registered_stations_to_moscow: list[StationDocumentModel] = [
            station for station in actual_stations_list if station.direction == self._station_direction.TO_MOSCOW
        ]
        for another_direction_station in await self._entity.get_all_registered_stations(direction, True):



            direct_schedule:  SchedulesBetweenStations = self._api_view.get_schedule(
                departure_station_code=another_direction_station.code,
                arrived_station_code=)
            schedules = [
                ScheduleDocumentModel(schedule=direct_schedule.ext(),
                                      arrived_station_code=another_direction_station.code,
                                      departure_station_code=code,
                                      update_time=datetime.now()),
                ScheduleDocumentModel(schedule=back_schedule.dict(),
                                      arrived_station_code=code,
                                      departure_station_code=another_direction_station.code,
                                      update_time=datetime.now())]
            await self.__entity.write_schedules(schedules)
        pass

    async def get_available_directions(self) -> Type[StationsDirection]:
        return self._station_direction

    async def register_station_with_direction(self):
        stations = await app.get_stations(self.__schedule_view, for_registration=True)
        text_direction = await app.admin_controller.get_text_direction(direction)
        register_action = app.admin_controller.get_register_action()

    async def get_text_direction(self, direction) -> str:
        return self._direction_validator(direction=direction).get_text_direction()

    async def get_edit_menu_values(self) -> tuple[str, str]:
        return self._action_enum.DELETE, self._action_enum.MOVE

    async def get_register_action(self) -> str:
        return self._action_enum.REGISTER

    @base_error_handler
    async def station_action(self, action: str, direction: str, code: str) -> None:
        actual_stations_list = []
        direction_object: DirectionType = self._direction_validator(direction=direction)
        try:
            match action:
                case self._action_enum.DELETE:
                    actual_stations_list: list[StationDocumentModel] = await self.__entity.delete_station(
                        code, direction_object.get_direction())
                case self._action_enum.MOVE:
                    actual_stations_list: list[StationDocumentModel] = await self.__entity.move_station(
                        code, direction_object.get_direction(),
                        direction_object.get_another())
                case self._action_enum.REGISTER:
                    actual_stations_list: list[StationDocumentModel] = await self.__entity.register_station(
                        await self.__schedule_view.get_station_by_api(direction_object.get_direction(), code)
                    )

        if actual_stations_list:
            await self.__call_change_station_callback(actual_stations_list)
        else:
            raise self._internal_error("Действие не вернуло актуальное сосотояние.")

