import asyncio
from dataclasses import dataclass
from typing import Type, TypeVar, Generic, Callable

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError

from src.services.db_client.collections import ScheduleDbCollection, RegisteredStationsDbClient
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import AuthError, ModelError


@dataclass
class Collections:
    schedule: ScheduleDbCollection
    stations: RegisteredStationsDbClient


DomainStationObject = TypeVar("DomainStationObject")
DomainScheduleObject = TypeVar("DomainScheduleObject")


class ScheduleEntity(Generic[DomainStationObject, DomainScheduleObject]):

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

    def set_on_station_change(self, callback: Callable):
        self.__on_station_change = callback

    async def __delete_related_schedule(self, station: StationDocumentModel):
        schedules = [schedule for schedule in self.collections.schedule.get_all_schedules()
                     if schedule.arrived_station_code == station.code or
                     schedule.departure_station_code == station.code]
        await asyncio.gather(*[self.collections.schedule.delete_schedule(schedule) for schedule in schedules])

    async def delete_station(self, code, direction) -> None:
        station: StationDocumentModel = await self.collections.stations.delete_station(code, direction)
        await self.__delete_related_schedule(station)
        await self.__on_station_change()

    async def move_station(self, code, direction) -> None:
        station: StationDocumentModel = await self.collections.stations.move_station(code, direction)
        await self.__delete_related_schedule(station)
        await self.__on_station_change()

    async def register_station(self, station: DomainStationObject) -> None:
        try:
            new_station = StationDocumentModel(**station.dict())
        except ValidationError:
            raise ModelError("Ошибка при создании модели станци.")
        await self.collections.stations.register_station(new_station)
        await self.__on_station_change()

    async def get_all_registered_stations(self, direction=None) -> list[DomainStationObject]:
        try:
            return [
                self._station_domain_model(**station.dict())
                for station in await self.collections.stations.get_all_registered_stations(direction)
            ]
        except ValidationError:
            raise ModelError("Данные получены в неверном формате")

    async def write_schedule(self, new_object: DomainScheduleObject):
        try:
            new_schedule = ScheduleDocumentModel(**new_object.dict())
        except ValidationError as e:
            raise ModelError(f"Ошибка при создании модели расписания. {str(e)}")
        await self.collections.schedule.write_schedule(new_schedule)

    async def get_schedule(self, departure_station_code, arrived_station_code):
        return await self.collections.schedule.get_schedule(departure_station_code, arrived_station_code)