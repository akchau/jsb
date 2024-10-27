"""
Модуль взаимодействия контроллера с БД.
"""
import asyncio
from dataclasses import dataclass

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError, BaseModel

from src.services.db_client.collections import ScheduleDbCollection, RegisteredStationsDbCollection
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import ModelError


class ScheduleEntity:
    """
    Взаимодействие контроллера с БД через коллекции.

    - Реализует интерфейс для контроллера для работы с базой данных.
    - С помощью ModelTransformator преобразует модели БД в доменные модели.
    """

    _auth_model: BaseModel = DbClientAuthModel
    _model_error: Exception = ModelError

    @classmethod
    def construct(cls, **kwargs):
        try:
            return cls(client_data=cls._auth_model(**kwargs))
        except ValidationError:
            raise ModelError("При пробросе данных авторизации произошла ошибка парсинга! Данные авторизации невалидны")

    def __init__(self, client_data: DbClientAuthModel):
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

    async def delete_station(self, code, direction) -> list[StationDocumentModel]:
        """
        Удаление станции.
        :param code: Код станции.
        :param direction: Направление в котором зарегистрирована станция.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.delete_station(code, direction)
        await self.__delete_related_schedule(station)
        return await self.get_all_registered_stations()

    async def move_station(self, code, direction, new_direction) -> list[StationDocumentModel]:
        """
        Перемещение станции.
        :param code: Код станции.
        :param direction: Текущее направление.
        :return:
        """
        station: StationDocumentModel = await self.collections.stations.move_station(code, direction, new_direction)
        await self.__delete_related_schedule(station)
        return await self.get_all_registered_stations()

    async def register_station(self, station: StationDocumentModel) -> list[StationDocumentModel]:
        """
        Регистрация станции.
        :param station: Новая станция.
        :return:
        """
        # TODO регистрация происходит наоборот
        await self.collections.stations.register_station(station)
        return await self.get_all_registered_stations()

    async def get_station_by_code(self, code: str, direction: str) -> StationDocumentModel:
        return await self.collections.stations.get_station(code, direction)

    async def get_all_registered_stations(self, direction=None,
                                          exclude_direction: bool = False) -> list[StationDocumentModel]:
        """
        Получение списка зарегистрированных станций.
        :param direction Направление.
        :param exclude_direction Исключить направление.
        :return:
        """
        return await self.collections.stations.get_all_registered_stations(direction, exclude_direction)

    async def write_schedules(self, new_objects: list[ScheduleDocumentModel]) -> None:
        """
        Запись расписаний.
        :param new_objects: Новые расписания.
        :return: None
        """
        [
            await self.collections.schedule.write_schedule(new_schedule)
            for new_schedule in new_objects
        ]

    async def get_schedule(self, departure_station_code: str,
                           arrived_station_code: str,
                           direction: str) -> ScheduleDocumentModel:
        """
        Получение расписания вместе со станциями.
        :param departure_station_code Код станции отправления.
        :param arrived_station_code Код станции прибытия.
        :param direction Направление станции отправления.
        :return:
        """
        schedule = await self.collections.schedule.get_schedule(departure_station_code, arrived_station_code)
        return schedule