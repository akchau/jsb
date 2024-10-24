import logging
from typing import Type

from src.domain.base import BaseApp
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


    async def edit_station_view(self, update):
        user = update.message.from_user if update.message else update.callback_query.from_user
        data: tuple[str, str] | None = await self.parse_data(update)
        direction, code = data
        station = await self._entity.get_station_by_code(code, direction)
        logger.debug(f"ID={user.id} вошел в меню станции {station.title} в направлении {direction}.")


    async def registered_stations_with_direction_view(self, update):
        user = update.message.from_user if update.message else update.callback_query.from_user
        parsed_data = await self.parse_data(update)
        if len(parsed_data) == 3:
            direction, action, code = parsed_data
            clean_direction = DirectionType(direction=direction)
            logger.debug(f"fID={user.id} {action} станцию {code} в направлении {direction}:")
            match action:
                case self._action_enum.DELETE:
                    await self._entity.delete_station(
                        code, clean_direction.get_direction())
                case self._action_enum.MOVE:
                    await self._entity.move_station(
                        code, clean_direction.get_direction(),
                        clean_direction.get_another())
                case self._action_enum.REGISTER:
                    await self._entity.register_station(
                        await self._api_view.get_station_by_api(clean_direction.get_direction(), code)
                    )
        else:
            direction = parsed_data
            clean_direction = DirectionType(direction=direction)
            logger.debug(
                f"ID={user.id} Просматривает список станций в направлении {clean_direction.get_text_direction()}.")
        registered_stations = await self._entity.get_all_registered_stations(clean_direction)
        return {

            "callback_data": [
                (
                    registered_station.title,
                    await self.create_data(clean_direction.get_direction(),registered_station.code)
                )
                for registered_station in registered_stations
            ],
            "text_direction": clean_direction.get_text_direction(),
            "direction": clean_direction.get_text_direction()
        }

    async def registered_stations_view(self, update):
        user = update.message.from_user if update.message else update.callback_query.from_user
        logger.debug(f"Пользователь: {user.id} выбирает направление станций")
        return  {
            "directions": [DirectionType(direction=direction).get_tuple()
                           for direction in self._station_direction.__members__]
        }

    async def register_station_view(self, update) -> dict:
        user = update.message.from_user if update.message else update.callback_query.from_user
        logger.debug(f"Пользователь: {user.id} выбирает направление для регистрации станций")
        return  {
            "directions": [DirectionType(direction=direction).get_tuple()
                           for direction in self._station_direction.__members__]
        }

    async def register_station_with_direction_view(self, update) -> dict:
        direction: str = await self.parse_data(update)
        clean_direction = DirectionType(direction=direction)
        user = update.message.from_user if update.message else update.callback_query.from_user
        logger.debug(f"Пользователь: {user} регистрирует станции в направлении {clean_direction.get_text_direction()}")
        all_stations: list[StationDocumentModel] = await self._api_view.get_all_stations_by_api()
        already_registered_stations: list[StationDocumentModel] = await self._entity.get_all_registered_stations(clean_direction.get_direction())
        return {

            "callback_data": [
                (not_registered_station.title, await self.create_data(clean_direction.get_direction(),not_registered_station.code))
                for not_registered_station in all_stations if not_registered_station not in already_registered_stations
            ],
            "text_direction": clean_direction.get_text_direction(),
            "direction": clean_direction.get_text_direction()
        }

