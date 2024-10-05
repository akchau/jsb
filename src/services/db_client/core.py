"""
Модуль взаимодействия контроллера с БД.
"""
import asyncio
from dataclasses import dataclass
from typing import Type, TypeVar, Generic

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError

from src.controller import controller_types
from src.services.db_client.collections import ScheduleDbCollection, RegisteredStationsDbClient
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import AuthError, ModelError, InternalDbError


@dataclass
class Collections:
    """
    Коллекции которые используются.
    """
    schedule: ScheduleDbCollection
    stations: RegisteredStationsDbClient


DomainStationObject = TypeVar("DomainStationObject")
DomainScheduleObject = TypeVar("DomainScheduleObject")


class ScheduleEntity(Generic[DomainStationObject, DomainScheduleObject]):
    """
    Взаимодействие контроллера с БД через коллекции.
    """

    #TODO передавать лучше строкой и вернуть проверку
    def __init__(self, db_name: str, db_host: str, dp_port: int, db_user: str, db_password: str,
                 station_domain_model: Type[DomainStationObject],
                 _transport_class: Type[MongoDbTransport] = MongoDbTransport):
        try:
            clean_data = DbClientAuthModel(
                db_name=db_name,
                db_host=db_host,
                db_port=dp_port,
                db_user=db_user,
                db_password=db_password
            )
        except ValidationError:
            raise AuthError("Невалидные данные для подключения к бд")

        transport = _transport_class(**clean_data.dict())

        self.collections = Collections(
            schedule=ScheduleDbCollection(
                transport,
                collection_model=ScheduleDocumentModel,
                collection_name="schedule"
            ),
            stations=RegisteredStationsDbClient(
                transport,
                collection_model=StationDocumentModel,
                collection_name="stations"
            )
        )
        self._station_domain_model = station_domain_model
        self.__on_station_change = None

    async def __delete_related_schedule(self, station: StationDocumentModel) -> None:
        """
        Удаление связанных станций.
        :param station: Станция.
        :return:
        """
        schedules = [schedule for schedule in self.collections.schedule.get_all_schedules()
                     if station.code in {schedule.arrived_station_code, schedule.departure_station_code}]
        await asyncio.gather(*[self.collections.schedule.delete_schedule(schedule) for schedule in schedules])

    async def get_station_condition(self) -> tuple[list[DomainStationObject], list[DomainStationObject]]:
        """
        В передаваемый колбек контролера передаем актуальное состояние станций.
        :return:
        """

        all_stations = await self.get_all_registered_stations()
        registered_stations_from_moscow = [station for station in all_stations
                                           if station.direction == controller_types.StationsDirection.FROM_MOSCOW]
        registered_stations_to_moscow = [station for station in all_stations
                                         if station.direction == controller_types.StationsDirection.TO_MOSCOW]

        return registered_stations_to_moscow, registered_stations_from_moscow

    async def delete_station(self, code, direction) -> tuple[list[DomainStationObject], list[DomainStationObject]]:
        """
        Удаление станции.
        :param code: Код станции.
        :param direction: Направление в котором зарегистрирована станция.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.delete_station(code, direction)
        await self.__delete_related_schedule(station)
        return await self.get_station_condition()

    async def move_station(self, code, direction) -> tuple[list[DomainStationObject], list[DomainStationObject]]:
        """
        Перемещение станции.
        :param code: Код станции.
        :param direction: Текущее направление.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.move_station(code, direction)
        await self.__delete_related_schedule(station)
        return await self.get_station_condition()

    async def register_station(self,
                               station: DomainStationObject
                               ) -> tuple[list[DomainStationObject], list[DomainStationObject]]:
        """
        Регистрация станции.
        :param station: Новая станция.
        :return:
        """
        try:
            new_station = StationDocumentModel(**station.dict())
        except ValidationError as e:
            raise ModelError(f"Ошибка при создании модели станци. {e}")
        await self.collections.stations.register_station(new_station)
        return await self.get_station_condition()

    async def get_all_registered_stations(self, direction=None) -> list[DomainStationObject]:
        """
        Получение списка зарегистрированных станций.
        :param direction:
        :return:
        """

        try:
            return [
                self._station_domain_model(**station.dict())
                for station in await self.collections.stations.get_all_registered_stations(direction)
            ]
        except ValidationError:
            raise ModelError("Данные получены в неверном формате")

    async def write_schedule(self, new_object: DomainScheduleObject) -> None:
        """
        Запись расписания.
        :param new_object: Новое расписание.
        :return: None
        """
        try:
            new_schedule = ScheduleDocumentModel(**new_object.dict())
        except ValidationError as e:
            raise ModelError(f"Ошибка при создании модели расписания. {str(e)}")
        await self.collections.schedule.write_schedule(new_schedule)

    async def get_schedule(self, departure_station_code, arrived_station_code) -> ScheduleDocumentModel:
        """
        Получение расписания.
        :param departure_station_code: Код станции отправления.
        :param arrived_station_code: Код станции прибытия.
        :return:
        """
        return await self.collections.schedule.get_schedule(departure_station_code, arrived_station_code)
