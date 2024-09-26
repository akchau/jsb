"""
Модуль взаимодействия контроллера с БД.
"""
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

    def set_on_station_change(self, callback: Callable) -> None:
        """
        Задание колбека при смене состава зарегистрированных станций.
        :param callback: Коллбек, который вызовется при смене состава зарегистрированных станций
        :return:
        """
        self.__on_station_change = callback

    async def __delete_related_schedule(self, station: StationDocumentModel) -> None:
        """
        Удаление связанных станций.
        :param station: Станция.
        :return:
        """
        schedules = [schedule for schedule in self.collections.schedule.get_all_schedules()
                     if station.code in {schedule.arrived_station_code, schedule.departure_station_code}]
        await asyncio.gather(*[self.collections.schedule.delete_schedule(schedule) for schedule in schedules])

    async def delete_station(self, code, direction) -> None:
        """
        Удаление станции.
        :param code: Код станции.
        :param direction: Направление в котором зарегистрирована станция.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.delete_station(code, direction)
        await self.__delete_related_schedule(station)
        await self.__on_station_change()

    async def move_station(self, code, direction) -> None:
        """
        Перемещение станции.
        :param code: Код станции.
        :param direction: Текущее направление.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.move_station(code, direction)
        await self.__delete_related_schedule(station)
        await self.__on_station_change()

    async def register_station(self, station: DomainStationObject) -> None:
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
        await self.__on_station_change()

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
