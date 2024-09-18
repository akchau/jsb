from typing import TypeVar, Generic

from mongo_db_client import MongoDbTransport

from src.controller.controller_types import StationsDirection
from src.services.db_client.exc import ExistException, NotExistException, DbClientException


Station = TypeVar("Station")


class RegisteredStationsDbClient(Generic[Station]):
    """
    Клиент зарегистрированных станций.

    - Получение списка станций.
    - Регистрация новой станции.
    """

    STATIONS_COLLECTION_NAME = "stations"

    def __init__(self, db_name, db_host, dp_port, db_user, db_password, _transport_class=MongoDbTransport):
        self.__transport = _transport_class(db_name, db_user, db_password, db_host, dp_port)

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
        """
        station = await self.__get_station_by_code_and_direction(code, direction)
        if station:
            self.__transport.update_field(
                collection_name=self.STATIONS_COLLECTION_NAME,
                field_name="direction",
                new_value=(StationsDirection.TO_MOSCOW if station["direction"] == StationsDirection.FROM_MOSCOW \
                           else StationsDirection.FROM_MOSCOW),
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
