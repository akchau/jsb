import logging
from datetime import datetime

from src.domain.base import BaseApp, app_handler
from src.domain.controller_types import DirectionType, StationsDirection, StationActionEnum, SchedulesBetweenStations
from src.domain.exc import InternalError
from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity, DbClientException
from src.services.db_client.db_client_types import StationDocumentModel, ScheduleDocumentModel


logger = logging.getLogger(__name__)


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



class StationsManager:

    def __init__(self, entity, api_view):
        self.__action_enum = StationActionEnum
        self.__entity = entity
        self.__api_view = api_view

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


    async def get_actions(self):
        return {
            "delete": self.__action_enum.DELETE,
            "move": self.__action_enum.MOVE,
            "register": self.__action_enum.REGISTER
        }

    async def station_action(self, direction: DirectionType, action: str, code: str) -> None:
        """
        Метод выполняет действие со станцией.
        :param action: Действие со станцией.
        :param code: Код стаанци.
        :param direction: Направление станци.
        :return:
        """
        match action:
            case self.__action_enum.DELETE:
                await self.__entity.delete_station(
                    code, direction.get_direction())
            case self.__action_enum.MOVE:
                await self.__entity.move_station(
                    code, direction.get_direction(),
                    direction.get_another())
            case self.__action_enum.REGISTER:
                await self.__entity.register_station(
                    await self.__api_view.get_station_by_api(direction.get_direction(), code)
                )



class AdminApp(BaseApp):

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        super().__init__(view, entity)
        self._internal_error = InternalError
        self._direction_validator = DirectionType
        self._station_direction = StationsDirection
        self.station_manger = StationsManager(entity=self._entity, api_view=self._api_view)

    @app_handler
    async def edit_station_view(self, user, data):
        direction, code = data
        station = await self._entity.get_station_by_code(code, direction)
        logger.debug(f"ID={user.id} вошел в меню станции {station.title} в направлении {direction}.")

    @app_handler
    async def registered_stations_with_direction_view(self, user, data):
        clean_direction = StationsDirection.FROM_MOSCOW
        if data is not None:
            clean_direction = DirectionType(direction=data["direction"])
            await self.station_manger.station_action(**data)

        logger.debug(f"ID={user.id} Просматривает список станций"
                     f" в направлении {clean_direction.get_text_direction()}.")

        registered_stations_in_direction = await self._entity.get_all_registered_stations(clean_direction)
        return {
            "registered_stations_buttons": [
                (
                    registered_station_in_direction.title,
                    await self._context_creator.create_data(
                        {
                            "direction": clean_direction.get_direction(),
                            "code": registered_station_in_direction.code
                        }
                    )
                )
                for registered_station_in_direction in registered_stations_in_direction
            ],
            "text_direction": clean_direction.get_text_direction(),
            "direction": clean_direction.get_text_direction()
        }

    @app_handler
    async def register_station_with_direction_view(self, user, data) -> dict:
        clean_direction = DirectionType(direction=data)
        logger.debug(f"Пользователь: {user} регистрирует станции в направлении {clean_direction.get_text_direction()}")
        all_stations: list[StationDocumentModel] = await self._api_view.get_all_stations_by_api()
        already_registered_stations: list[StationDocumentModel] = await self._entity.get_all_registered_stations(clean_direction.get_direction())
        return {

            "available_stations_buttons": [
                (
                    not_registered_station.title,
                    await self._context_creator.create_data(
                        {
                            "direction": clean_direction.get_direction(),
                            "code": not_registered_station.code
                        }
                    )
                )
                for not_registered_station in all_stations if not_registered_station not in already_registered_stations
            ],
            "text_direction": clean_direction.get_text_direction(),
            "direction": clean_direction.get_text_direction()
        }

