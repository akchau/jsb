"""
Главный модуль контроллера.
"""
import logging
from datetime import datetime
from typing import Type

from .controller_types import StationActionEnum, StationsDirection, Station, DirectionType, Schedule
from .exc import InternalError

from src.services import ApiInteractor, ScheduleEntity, ExistException, ApiError, DbClientException
from .send_schedule import DataConstructor


logger = logging.getLogger(__name__)


class ScheduleController:
    """
    Главный класс контоллера.
    """

    def __init__(self, base_url: str, api_key: str, base_station_code: str, pagination: int, **kwargs):
        self._station_model = Station
        self._entity = ScheduleEntity.construct(**kwargs, station_domain_model=self._station_model)
        self._api = ApiInteractor(base_url, api_key, base_station_code)
        self._api_error = ApiError
        self._internal_error = InternalError
        self._db_client_error = DbClientException
        self._schedule_model = Schedule
        self._direction_validator = DirectionType
        self._station_direction = StationsDirection
        self._action_enum = StationActionEnum
        self._schedule_constructor = DataConstructor(pagination)

    async def change_station_callback(self, actual_condition: tuple[list[Station], list[Station]]):
        """
        Колбек который вызвывается при изменении состава станций.
        :param actual_condition:
        :return:
        """

        pass

    async def station_action(self, action: str, direction: str, code: str) -> None:
        actual_stations_list = None
        clean_direction: StationsDirection = self._direction_validator(direction=direction).get_direction()
        try:
            match action:
                case self._action_enum.DELETE:
                    actual_stations_list = await self._entity.delete_station(code, clean_direction)
                case self._action_enum.MOVE:
                    new_value = self._station_direction.TO_MOSCOW \
                        if clean_direction == self._station_direction.FROM_MOSCOW else self._station_direction.FROM_MOSCOW
                    actual_stations_list = await self._entity.move_station(code, clean_direction, new_value)
                case self._action_enum.REGISTER:
                    try:
                        list_stops_from_api: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
                        all_stations = [self._station_model(**stop, direction=clean_direction)
                                        for stop in list_stops_from_api]
                        for available_station in all_stations:
                            if available_station.code == code:
                                actual_stations_list = await self._entity.register_station(available_station)
                                for another_direction_station in await self._entity.get_all_registered_stations(
                                        direction, True):
                                    direct_schedule, back_schedule = await self._api.get_schedule(another_direction_station.code, code)
                                    schedules = [
                                        Schedule(schedule=direct_schedule,
                                                 arrived_station_code=another_direction_station.code,
                                                 departure_station_code=code,
                                                 update_time=datetime.now()),
                                        Schedule(schedule=back_schedule,
                                                 arrived_station_code=code,
                                                 departure_station_code=another_direction_station.code,
                                                 update_time=datetime.now())]
                                    await self._entity.write_schedules(schedules)
                    except ExistException:
                        pass
                    except self._api_error as e:
                        raise self._internal_error(str(e))
            if actual_stations_list:
                registered_stations_from_moscow: list[Station] = [
                    station for station in actual_stations_list
                    if station.direction == self._station_direction.FROM_MOSCOW
                ]
                registered_stations_to_moscow: list[Station] = [
                    station for station in actual_stations_list
                    if station.direction == self._station_direction.TO_MOSCOW
                ]
                await self.change_station_callback(
                    (registered_stations_from_moscow, registered_stations_to_moscow)
                )
            else:
                raise self._internal_error("Действие не вернуло актуальное сосотояние.")
        except self._db_client_error as e:
            raise self._internal_error(str(e))

    async def get_stations_for_schedule(self, direction=None, exclude_direction: bool = False):
        if direction:
            return await self._entity.get_all_registered_stations(direction, exclude_direction=exclude_direction)
        return await self._entity.get_all_registered_stations(direction)

    async def get_stations_for_admin(self, direction: str, for_registration: bool = False) -> list[Station]:
        logger.debug(f"Получение стаций в меню администартора в направлнеии {direction}, по api={for_registration}")
        if for_registration and direction:
            try:
                list_stops_from_api: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
            except self._api_error:
                raise self._internal_error("Ошибка api.")
            all_stations = [self._station_model(**stop,
                                                direction=self._direction_validator(
                                                    direction=direction).get_direction())
                            for stop in list_stops_from_api]
            already_registered_stations: list[Station] = await self._entity.get_all_registered_stations(direction)
            return [station for station in all_stations if station not in already_registered_stations]
        else:
            return await self._entity.get_all_registered_stations(direction)

    async def get_directions(self) -> Type[StationsDirection]:
        return self._station_direction

    async def get_text_direction(self, direction) -> str:
        return self._direction_validator(direction=direction).get_text_direction()

    async def get_edit_menu_values(self) -> tuple[str, str]:
        return self._action_enum.DELETE, self._action_enum.MOVE

    async def get_register_action(self) -> str:
        return self._action_enum.REGISTER

    async def get_schedule(self, departure_station_code: str,
                           arrived_station_code: str, direction: str) -> tuple[str, Station, Station]:
        schedule, departure_station, arrived_station = await self._entity.get_schedule(
            departure_station_code,
            arrived_station_code,
            direction
        )
        return (
            self._schedule_constructor.constructor(
                schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            departure_station,
            arrived_station
        )

