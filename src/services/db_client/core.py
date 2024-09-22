import datetime
import time
from typing import TypeVar, Generic

from mongo_db_client import MongoDbTransport
from pydantic import ValidationError

from src.controller.controller_types import StationsDirection
from src.services.db_client.base import BaseDbClient
from src.services.db_client.db_client_types import DbClientAuthModel, ScheduleModel
from src.services.db_client.exc import ExistException, NotExistException, DbClientException, AuthError, ModelError

Station = TypeVar("Station")


class ScheduleDbClient(BaseDbClient):

    SCHEDULE_COLLECTION_NAME = "schedule"

    async def get_schedule(self, departure_station_code: str, arrived_station_code) -> ScheduleModel | None:
        """
        Получение расписания по кодам станций

        :param departure_station_code: Код станции отправления.
        :param arrived_station_code: Код станции прибытия.
        :return:
        """
        schedules = [ScheduleModel(**schedule, id=str(schedule["_id"]))
                     for schedule in self._transport.get_list(self.SCHEDULE_COLLECTION_NAME)]
        for schedule in schedules:
            if (schedule.departure_station_code == departure_station_code and
                    schedule.arrived_station_code == arrived_station_code):
                return schedule
        return None

    async def write_schedule(self, departure_station_code: str, arrived_station_code: str,
                             schedule_data: list[tuple]) -> ScheduleModel | None:
        """
        Зарегистрировать станцию.
        """
        try:
            new_schedule = ScheduleModel(
                arrived_station_code=arrived_station_code,
                departure_station_code=departure_station_code,
                update_time=datetime.datetime.now(),
                schedule=schedule_data
            )
        except ValidationError:
            raise ModelError("Ошибка при создании модели расписания.")

        this_schedule = await self.get_schedule(new_schedule.departure_station_code,
                                                new_schedule.arrived_station_code)
        if this_schedule:
            self._transport.delete(collection_name=self.SCHEDULE_COLLECTION_NAME, instance_id=this_schedule.id)
        self._transport.post(self.SCHEDULE_COLLECTION_NAME, new_schedule.create_document())
        created_schedule = await self.get_schedule(new_schedule.departure_station_code,
                                                   new_schedule.arrived_station_code)
        if created_schedule is None:
            raise DbClientException("Расписание не добавлено!")
        return created_schedule


# TODO перенести слой с подтверждением удаления  в отдельный слой, а клиент только для логики БД???
class RegisteredStationsDbClient(Generic[Station]):
    """
    Клиент зарегистрированных станций.

    - Получение списка станций.
    - Регистрация новой станции.
    """

    STATIONS_COLLECTION_NAME = "stations"

    def __init__(self, db_name: str, db_host: str, dp_port: int, db_user: str, db_password: str,
                 _transport_class=MongoDbTransport):
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
        self.__transport = _transport_class(**clean_data.dict())

    async def __get_station_by_code_and_direction(self, code: str, direction: StationsDirection) -> dict | None:
        all_stations = self.__transport.get_list(collection_name=self.STATIONS_COLLECTION_NAME)
        result = [station for station in all_stations
                  if station["code"] == code and station["direction"] == direction]
        if len(result) == 0:
            return None
        return result[0]

    async def get_all_registered_stations(self, direction: StationsDirection) -> list[dict]:
        """
        Получить все зарегестрированные станции.
        :param direction: Направление, в котором ищутся зарегестрированные станции.
        :return: Список станций, зарегистрированных в данном направлении.
        """
        # TODO тут можно проверять, что поле имеет атрибут direction
        all_stations: list[dict] = self.__transport.get_list(collection_name=self.STATIONS_COLLECTION_NAME)
        return [station for station in all_stations if station["direction"] == direction]

    async def register_station(self, station: dict) -> dict:
        """
        Зарегистрировать станцию.
        :param station: Данные станции.
        :return: Данные станции.
        """
        #TODO прикрутить валидацию полей необходимых для работы клиента
        station_code = station["code"]
        station_direction = station["direction"]

        this_station = await self.__get_station_by_code_and_direction(station_code, station_direction)
        if this_station is None:
            self.__transport.post(self.STATIONS_COLLECTION_NAME, station)
            created_station = await self.__get_station_by_code_and_direction(station_code, station_direction)
            if created_station is None:
                raise DbClientException("Станция не зарегистриоовалась!")
            return created_station
        else:
            raise ExistException

    async def delete_station(self, code: str, direction: StationsDirection) -> dict:
        """
        Удалить станцию.
        :param code: Код станци.
        :param direction: Направление, удаляемой станции.
        :return: Данные станции.
        """

        station = await self.__get_station_by_code_and_direction(code, direction)
        if station:
            self.__transport.delete(collection_name=self.STATIONS_COLLECTION_NAME,
                                    instance_id=station["_id"])
            deleted_station = await self.__get_station_by_code_and_direction(code, direction)
            if deleted_station:
                raise DbClientException("Станция не удалилась")
            return station
        else:
            raise NotExistException

    async def move_station(self, code: str, direction: StationsDirection) -> dict:
        """
        Переместить станцию.
        :param code: Код станци.
        :param direction: Направление, удаляемой станции.
        :return: Обновленные данные станции.
        """
        station = await self.__get_station_by_code_and_direction(code, direction)
        if station:

            new_value = (StationsDirection.TO_MOSCOW if station["direction"] == StationsDirection.FROM_MOSCOW \
                         else StationsDirection.FROM_MOSCOW)

            self.__transport.update_field(
                collection_name=self.STATIONS_COLLECTION_NAME,
                field_name="direction",
                new_value=new_value,
                instance_id=station["_id"])
            updated_station = self.__transport.get(
                    collection_name=self.STATIONS_COLLECTION_NAME,
                    instance_id=station["_id"]
            )
            if updated_station is None or updated_station["direction"] == station["direction"]:
                raise DbClientException("Поле не обновилось")
            return updated_station
        else:
            raise NotExistException
