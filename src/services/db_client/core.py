"""
Модуль взаимодействия контроллера с БД.
"""
import asyncio
from dataclasses import dataclass
from typing import Type, TypeVar, Generic

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError

from src.services.db_client.collections import ScheduleDbCollection, RegisteredStationsDbCollection
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import ModelError


@dataclass
class Collections:
    """
    Коллекции которые используются.
    """
    schedule: ScheduleDbCollection
    stations: RegisteredStationsDbCollection


DomainStationObject = TypeVar("DomainStationObject")
DomainScheduleObject = TypeVar("DomainScheduleObject")


class ScheduleEntity(Generic[DomainStationObject, DomainScheduleObject]):
    """
    Взаимодействие контроллера с БД через коллекции.
    """

    _auth_model = DbClientAuthModel

    @classmethod
    def construct(cls, station_domain_model, **kwargs):
        return cls(client_data=cls._auth_model(**kwargs), station_domain_model=station_domain_model)

    #TODO передавать лучше строкой и вернуть проверку
    def __init__(self, station_domain_model, client_data: DbClientAuthModel):
        transport = MongoDbTransport(**client_data.dict())

        self.collections = Collections(
            schedule=ScheduleDbCollection(
                transport,
                collection_name="schedule"
            ),
            stations=RegisteredStationsDbCollection(
                transport,
                collection_name="stations"
            )
        )
        self._station_domain_model = station_domain_model
        self._model_error = ModelError
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

    async def delete_station(self, code, direction) -> list[DomainStationObject]:
        """
        Удаление станции.
        :param code: Код станции.
        :param direction: Направление в котором зарегистрирована станция.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.delete_station(code, direction)
        await self.__delete_related_schedule(station)
        return await self.get_all_registered_stations()


    async def move_station(self, code, direction, new_direction) -> list[DomainStationObject]:
        """
        Перемещение станции.
        :param code: Код станции.
        :param direction: Текущее направление.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.move_station(code, direction, new_direction)
        await self.__delete_related_schedule(station)
        return await self.get_all_registered_stations()

    async def register_station(self,
                               station: DomainStationObject
                               ) -> list[DomainStationObject]:
        """
        Регистрация станции.
        :param station: Новая станция.
        :return:
        """
        try:
            new_station = StationDocumentModel(**station.dict())
        except ValidationError as e:
            raise self._model_error(f"Ошибка при создании модели станци. {e}")
        await self.collections.stations.register_station(new_station)
        return await self.get_all_registered_stations()

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
            raise self._model_error("Данные получены в неверном формате")

    async def write_schedule(self, new_object: DomainScheduleObject) -> None:
        """
        Запись расписания.
        :param new_object: Новое расписание.
        :return: None
        """
        try:
            new_schedule = ScheduleDocumentModel(**new_object.dict())
        except ValidationError as e:
            raise self._model_error(f"Ошибка при создании модели расписания. {str(e)}")
        await self.collections.schedule.write_schedule(new_schedule)

    async def get_schedule(self, departure_station_code, arrived_station_code) -> ScheduleDocumentModel:
        """
        Получение расписания.
        :param departure_station_code: Код станции отправления.
        :param arrived_station_code: Код станции прибытия.
        :return:
        """
        return await self.collections.schedule.get_schedule(departure_station_code, arrived_station_code)
