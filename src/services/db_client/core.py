"""
Модуль взаимодействия контроллера с БД.
"""
import asyncio
from dataclasses import dataclass
from typing import TypeVar, Generic, Type

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError, BaseModel

from src.services.db_client.collections import ScheduleDbCollection, RegisteredStationsDbCollection
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import ModelError


DomainStationObject = TypeVar("DomainStationObject")
DomainScheduleObject = TypeVar("DomainScheduleObject")

TransformedModel = TypeVar("TransformedModel")


#TODO Класс преобразователь
class ModelTransformator(Generic[TransformedModel]):
    """
    Трансформатор моделей
    """

    def __init__(self, model_error: Exception):
        self.model_error = model_error

    async def transform(self, model: BaseModel, target_model: Type[TransformedModel]) -> TransformedModel:
        """
        Преобразование одной модели в другую.
        :param model:
        :param target_model:
        :return:
        """
        try:
            return target_model(**model.dict())
        except ValidationError:
            raise


class ScheduleEntity(Generic[DomainStationObject, DomainScheduleObject]):
    """
    Взаимодействие контроллера с БД через коллекции.

    - Реализует интерфейс для контроллера для работы с базой данных.
    - С помощью ModelTransformator преобразует модели БД в доменные модели.
    """

    _auth_model: BaseModel = DbClientAuthModel
    _model_error: Exception = ModelError

    @classmethod
    def construct(cls, station_domain_model: Type[BaseModel], **kwargs):
        try:
            return cls(client_data=cls._auth_model(**kwargs), station_domain_model=station_domain_model)
        except ValidationError:
            raise ModelError("При пробросе данных авторизации произошла ошибка парсинга! Данные авторизации невалидны")

    def __init__(self, station_domain_model: Type[BaseModel], client_data: DbClientAuthModel):
        transport = MongoDbTransport(**client_data.dict())
        @dataclass
        class Collections:
            """
            Коллекции которые используются.
            """
            schedule: ScheduleDbCollection
            stations: RegisteredStationsDbCollection

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
        self.__model_transformator = ModelTransformator(self._model_error)
        self.__on_station_change = None

    async def __delete_related_schedule(self, station: StationDocumentModel) -> None:
        """
        Удаление связанных станций.
        :param station: Станция которую удаляем.
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

    async def register_station(self, station: DomainStationObject) -> list[DomainStationObject]:
        """
        Регистрация станции.
        :param station: Новая станция.
        :return:
        """
        # TODO регистрация происходит наоборот

        new_station: StationDocumentModel = await self.__model_transformator.transform(station,
                                                                                       StationDocumentModel)
        await self.collections.stations.register_station(new_station)
        return await self.get_all_registered_stations()

    async def get_all_registered_stations(self, direction=None, exclude_direction: bool = False) -> list[DomainStationObject]:
        """
        Получение списка зарегистрированных станций.
        :param direction Направление.
        :param exclude_direction Исключить направление.
        :return:
        """
        return [
            await self.__model_transformator.transform(station, self._station_domain_model)
            for station in await self.collections.stations.get_all_registered_stations(direction, exclude_direction)
        ]

    async def write_schedules(self, new_objects: list[DomainScheduleObject]) -> None:
        """
        Запись расписания.
        :param new_object: Новое расписание.
        :return: None
        """
        new_schedules = [
            self.__model_transformator.transform(new_object, ScheduleDocumentModel)
            for new_object in new_objects
        ]
        [
            await self.collections.schedule.write_schedule(new_schedule)
            for new_schedule in new_schedules
        ]

    async def get_schedule(self, departure_station_code: str, arrived_station_code: str, direction: str):
        """
        Получение расписания.
        :param departure_station_code Код станции отправления.
        :param arrived_station_code Код станции прибытия.
        :param direction Направление станции отправления.
        :return:
        """
        departure_station = await self.collections.stations.get_station(departure_station_code, direction)
        arrived_station = await self.collections.stations.get_station(arrived_station_code, direction,
                                                                      exclude_direction=True)
        print(departure_station, arrived_station)
        return (await self.collections.schedule.get_schedule(departure_station_code, arrived_station_code),
                await self.__model_transformator.transform(departure_station, self._station_domain_model),
                await self.__model_transformator.transform(arrived_station, self._station_domain_model))