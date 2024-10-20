"""
Главный модуль контроллера.
"""
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Type

from .api_view import ApiView
from .controller_types import StationActionEnum, StationsDirection, DirectionType
from .exc import InternalError

from src.services import ScheduleEntity, DbClientException
from .send_schedule import DataConstructor
from ..services.api_client.api_client_types import StoreType
from ..services.api_client.core import TransportApiClient
from ..services.db_client.db_client_types import StationDocumentModel, ScheduleDocumentModel

logger = logging.getLogger(__name__)



class AdminApp:

    def __init__(self, view: ApiView, entity: ScheduleEntity):
        self.__schedule_view = view
        self.__entity = entity

        self._internal_error = InternalError
        self._db_client_error = DbClientException
        self._direction_validator = DirectionType
        self._station_direction = StationsDirection
        self._action_enum = StationActionEnum
        self._parsing_api_error = InternalError


    async def __call_change_station_callback(self, actual_stations_list: list[StationDocumentModel]):
        registered_stations_from_moscow: list[StationDocumentModel] = [
            station for station in actual_stations_list if station.direction == self._station_direction.FROM_MOSCOW
        ]
        registered_stations_to_moscow: list[StationDocumentModel] = [
            station for station in actual_stations_list if station.direction == self._station_direction.TO_MOSCOW
        ]
        for another_direction_station in await self.__entity.get_all_registered_stations(direction, True):
            direct_schedule = self.__schedule_view.get_schedule(departure_station_code=another_direction_station.code,
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
        except self._db_client_error as e:
            raise self._internal_error(str(e))
        if actual_stations_list:
            await self.__call_change_station_callback(actual_stations_list)
        else:
            raise self._internal_error("Действие не вернуло актуальное сосотояние.")


class ScheduleApp:

    def __init__(self, pagination: int, view: ApiView, entity: ScheduleEntity):
        self.__schedule_view = view
        self.__entity = entity
        self.__schedule_constructor = DataConstructor(pagination)

    async def get_stations(self, direction, for_registration: bool = False) -> list[StationDocumentModel]:
        """
        Выдает контекст на стадии ввода станций
        :param direction: Напарваленеи
        :param for_registration:
        :return:
        """
        if for_registration and direction:
            return [station for station in await self.__schedule_view.get_all_stations_by_api(direction)
                    if station not in await self.__entity.get_all_registered_stations(direction)]
        else:
            return await self.__entity.get_all_registered_stations(direction)

    async def get_schedule(self, departure_station_code: str, arrived_station_code: str,
                           direction: str) -> tuple[str, StationDocumentModel, StationDocumentModel]:
        schedule, departure_station, arrived_station = await self.__entity.get_schedule(departure_station_code,
                                                                                       arrived_station_code, direction)
        return (
            self.__schedule_constructor.constructor(
                schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            departure_station,
            arrived_station
        )



class Controller:

    def __init__(self, pagination: int, base_url: str, api_key: str, base_station_code: str, **kwargs):
        self.__entity = ScheduleEntity.construct(**kwargs)
        self.__store_type = StoreType
        self.__api_transport = TransportApiClient(
            base_url=base_url,
            api_prefix="v3.0",
            store=self.__store_type(
                api_key=api_key,
                base_station_code=base_station_code
            ),
            time_sleep=1,
            iterations=3
        )
        self.__view = ApiView(self.__api_transport,
                              station_model=StationDocumentModel, schedule_model=ScheduleDocumentModel)

        @dataclass
        class Apps:
            schedule: ScheduleApp
            admin: AdminApp

        self.__apps = Apps(
            schedule=ScheduleApp(view=self.__view, entity=self.__entity, pagination=pagination),
            admin=AdminApp(view=self.__view, entity=self.__entity)
        )

    def app(self, app: str):
        return getattr(self.__apps, app)