"""
Главный модуль контроллера.
"""
import logging
from datetime import datetime
from typing import Type

from api_client import RequestException
from pydantic import ValidationError

from .controller_types import StationActionEnum, StationsDirection, Station, DirectionType, Schedule
from .exc import InternalError

from src.services import ScheduleEntity, ApiError, DbClientException
from .send_schedule import DataConstructor
from ..services.api_client.api_client_types import StoreType
from ..services.api_client.core import TransportApiClient

logger = logging.getLogger(__name__)


class ApiInteractor:
    """
    Интерактор для работы с API.
    """
    def __init__(self, base_url: str, api_key: str, base_station_code: str):
        self._store_type = StoreType
        self.__api_client = TransportApiClient(
            base_url=base_url,
            api_prefix="v3.0",
            store=self._store_type(
                api_key=api_key,
                base_station_code=base_station_code
            ),
            time_sleep=1,
            iterations=3
        )

    async def get_schedule(self, departure_station_code, arrived_station_code):
        try:
            direct = await self.__api_client.get_schedule(departure_station_code, arrived_station_code)
            back = await self.__api_client.get_schedule(arrived_station_code, departure_station_code)
            return direct.ext(), back.ext()
        except RequestException as e:
            raise self._internal_api_error(str(e))
        except ValidationError as e:
            raise self._parsing_api_error(f"Ошибка валидации ответа API {str(e)}")

    async def get_all_stations_for_base_stations_thread(self) -> list[dict]:
        """
        Получение списка станций или станции по коду.
        """
        try:
            branch = await self.__api_client.get_branch_info()
            thread = await self.__api_client.get_thread_info(branch.get_thread_uid())
            return thread.ext_get_stations()
        except RequestException as e:
            raise self._internal_api_error(str(e))
        except ValidationError as e:
            raise self._parsing_api_error(f"Ошибка валидации ответа API {str(e)}")


class AdminController:

    def __init__(self, base_url: str, api_key: str, base_station_code: str, **kwargs):
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

    async def __get_all_stations_by_api(self, direction: StationsDirection) -> list[Station]:
        try:
            stations: list[dict] = await self._api.get_all_stations_for_base_stations_thread()
            return [self._station_model(**station, direction=direction) for station in stations]
        except self._api_error:
            raise self._internal_error("Ошибка api.")

    async def __get_station_by_api(self, direction: StationsDirection, code: str):
        stations: list[Station] = await self.__get_all_stations_by_api(direction)
        for station in stations:
            if station.code == code:
                return station

    async def __call_change_station_callback(self, actual_stations_list):
        registered_stations_from_moscow: list[Station] = [station for station in actual_stations_list
                                                          if station.direction == self._station_direction.FROM_MOSCOW]
        registered_stations_to_moscow: list[Station] = [station for station in actual_stations_list
                                                        if station.direction == self._station_direction.TO_MOSCOW]
        await self.change_station_callback((registered_stations_from_moscow, registered_stations_to_moscow))

    async def get_station(self, code, direction):
        return await self._entity.get_station_by_code(code, direction)

    async def get_directions(self) -> Type[StationsDirection]:
        return self._station_direction

    async def get_text_direction(self, direction) -> str:
        return self._direction_validator(direction=direction).get_text_direction()

    async def get_edit_menu_values(self) -> tuple[str, str]:
        return self._action_enum.DELETE, self._action_enum.MOVE

    async def get_register_action(self) -> str:
        return self._action_enum.REGISTER

    async def station_action(self, action: str, direction: str, code: str) -> None:
        actual_stations_list = None
        direction_object: DirectionType = self._direction_validator(direction=direction)
        try:
            match action:
                case self._action_enum.DELETE:
                    actual_stations_list: list[Station] = await self._entity.delete_station(
                        code, direction_object.get_direction())
                case self._action_enum.MOVE:
                    actual_stations_list = await self._entity.move_station(
                        code, direction_object.get_direction(),
                        direction_object.get_another())
                case self._action_enum.REGISTER:
                    actual_stations_list = await self._entity.register_station(
                        await self.__get_station_by_api(direction_object.get_direction(), code)
                    )
        except self._db_client_error as e:
            raise self._internal_error(str(e))
        if actual_stations_list:
            await self.__call_change_station_callback(actual_stations_list)
        else:
            raise self._internal_error("Действие не вернуло актуальное сосотояние.")

    async def get_stations(self, direction: str, for_registration: bool = False) -> list[Station]:
        clean_direction: StationsDirection = self._direction_validator(direction=direction).get_direction()
        logger.debug(f"Получение стаций в меню администартора в направлнеии {clean_direction}, по api={for_registration}")
        if for_registration and direction:
            return [station for station in await self.__get_all_stations_by_api(clean_direction)
                    if station not in await self._entity.get_all_registered_stations(direction)]
        else:
            return await self._entity.get_all_registered_stations(direction)

    async def change_station_callback(self, actual_condition: tuple[list[Station], list[Station]]):
        """
        Колбек который вызвывается при изменении состава станций.
        :param actual_condition:
        :return:
        """
        logger.debug(f"Произошло изменение состояния зарегистрированных станций, в {actual_condition}")
        for another_direction_station in await self._entity.get_all_registered_stations(direction, True):
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
        pass


class ScheduleController:
    """
    Главный класс контоллера.
    """

    def __init__(self, pagination: int, **kwargs):
        self._station_model = Station
        self._entity = ScheduleEntity.construct(**kwargs, station_domain_model=self._station_model)
        self._internal_error = InternalError
        self._db_client_error = DbClientException
        self._schedule_model = Schedule
        self._schedule_constructor = DataConstructor(pagination)

    async def get_stations(self, direction=None, exclude_direction: bool = False):
        if direction:
            return await self._entity.get_all_registered_stations(direction, exclude_direction=exclude_direction)
        return await self._entity.get_all_registered_stations(direction)

    async def get_schedule(self, departure_station_code: str, arrived_station_code: str,
                           direction: str) -> tuple[str, Station, Station]:
        schedule, departure_station, arrived_station = await self._entity.get_schedule(departure_station_code,
                                                                                       arrived_station_code, direction)
        return (
            self._schedule_constructor.constructor(
                schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            departure_station,
            arrived_station
        )

