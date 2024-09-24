from typing import TypeVar, Generic

from mongo_db_client.mongo_db_exceptions import BaseMongoTransportException
from pydantic import ValidationError, BaseModel

from src.controller.controller_types import StationsDirection
from src.services.db_client.base import BaseDbCollection
from src.services.db_client.db_client_types import ScheduleDocumentModel, StationDocumentModel
from src.services.db_client.exc import ExistException, NotExistException, DbClientException, ModelError, TransportError

DomainStationObject = TypeVar("DomainStationObject")
DomainScheduleObject = TypeVar("DomainScheduleObject")


class ScheduleDbCollection(BaseDbCollection):

    async def get_schedule(self, departure_station_code: str, arrived_station_code) -> ScheduleDocumentModel | None:
        """
        Получение расписания по кодам станций.

        :param departure_station_code: Код станции отправления.
        :param arrived_station_code: Код станции прибытия.
        :return:
        """
        schedules = self._transport.get_list(self._collection_name, model=ScheduleDocumentModel)
        for schedule in schedules:
            if (schedule.departure_station_code == departure_station_code and
                    schedule.arrived_station_code == arrived_station_code):
                return schedule
        return None

    async def delete_schedule(self, departure_station_code: str, arrived_station_code) -> ScheduleDocumentModel:
        """
        Удалить станцию.
        :param code: Код станци.
        :param direction: Направление, удаляемой станции.
        :return: Данные станции.
        """

        schedule = await self.get_schedule(departure_station_code, arrived_station_code)
        if schedule:
            self._transport.delete(collection_name=self._collection_name,
                                   instance_id=schedule.id)
            deleted_schedule = await self.get_schedule(departure_station_code, arrived_station_code)
            if deleted_schedule:
                raise DbClientException("Станция не удалилась")
            return schedule
        else:
            raise NotExistException

    async def write_schedule(self, new_object: DomainScheduleObject | dict) -> ScheduleDocumentModel:
        """
        Зарегистрировать станцию.
        """

        # TODO тест-кейсы
        # 1. Создание из валидного словаря.
        # 2. Создание из валидной модели.
        # 3. Создание из невалидного слоавря.
        # 4. Создание из невалидной модели.
        # 5. Создание из другого типа.
        # 6. После валидного создания подобное расписание уже существует
        # 7. После валидного создания подобное расписание не существует
        # 8-12. Транспорт ошибка в каждом вызове трпнспорта
        # 13. После успешного создания не существует.

        try:
            try:
                if isinstance(new_object, BaseModel):
                    new_model = self._collection_model(**new_object.dict())
                elif isinstance(new_object, dict):
                    new_model = ScheduleDocumentModel(**new_object)
                else:
                    raise ModelError("Неизвестный тип для парсинга в модель.")
            except ValidationError as e:
                raise ModelError(f"Ошибка при создании модели расписания. {str(e)}")

            # Если такое уже существует просто обновим.
            this_object = await self.get_schedule(new_model.departure_station_code,
                                                  new_model.arrived_station_code)
            if this_object:
                self._transport.delete(collection_name=self._collection_name, instance_id=this_object.id)

            self._transport.post(self._collection_name, new_model.create_document())

            # Проверяем что создалось
            created_object = await self.get_schedule(new_model.departure_station_code,
                                                     new_model.arrived_station_code)
            if created_object is None:
                raise DbClientException("Расписание не добавлено!")
            return created_object
        except BaseMongoTransportException as e:
            raise TransportError(str(e))


# TODO перенести слой с подтверждением удаления  в отдельный слой, а клиент только для логики БД???
class RegisteredStationsDbClient(BaseDbCollection, Generic[DomainStationObject]):
    """
    Клиент зарегистрированных станций.

    - Получение списка станций.
    - Регистрация новой станции.
    """

    async def __get_station(self, code: str, direction: StationsDirection) -> StationDocumentModel | None:
        all_stations_in_direction = await self.get_all_registered_stations(direction)
        result = [station for station in all_stations_in_direction
                  if station.code == code]
        if len(result) == 0:
            return None
        return result[0]

    async def get_all_registered_stations(self, direction: StationsDirection = None) -> list[StationDocumentModel]:
        """
        Получить все зарегестрированные станции.
        :param direction: Направление, в котором ищутся зарегестрированные станции.
        :return: Список станций, зарегистрированных в данном направлении.
        """
        try:
            all_stations: list[StationDocumentModel] = self._transport.get_list(collection_name=self._collection_name,
                                                                                model=StationDocumentModel)
        except ValidationError:
            raise ModelError("Ошибка при получении списка зарегистрированных станций")

        # При необходимости есть фильтрация по direction
        if direction is not None:
            return [station for station in all_stations if station.direction == direction]
        return all_stations

    async def register_station(self, station: DomainStationObject) -> StationDocumentModel:
        """
        Зарегистрировать станцию.
        :param station: Данные станции.
        :return: Данные станции.
        """

        try:
            new_station = self._collection_model(**station.dict())
        except ValidationError:
            raise ModelError("Ошибка при создании модели станци.")

        this_station: StationDocumentModel | None = await self.__get_station(new_station.code, new_station.direction)
        if this_station is None:
            self._transport.post(self._collection_name, new_station.create_document())
            created_station = await self.__get_station(new_station.code, new_station.direction)
            if created_station is None:
                raise DbClientException("Станция не зарегистриоовалась!")
            return created_station
        else:
            raise ExistException

    async def delete_station(self, code: str, direction: StationsDirection) -> StationDocumentModel:
        """
        Удалить станцию.
        :param code: Код станци.
        :param direction: Направление, удаляемой станции.
        :return: Данные станции.
        """

        station = await self.__get_station(code, direction)
        if station:
            self._transport.delete(collection_name=self._collection_name,
                                   instance_id=station.id)
            deleted_station = await self.__get_station(code, direction)
            if deleted_station:
                raise DbClientException("Станция не удалилась")
            return station
        else:
            raise NotExistException

    async def move_station(self, code: str, direction: StationsDirection) -> StationDocumentModel:
        """
        Переместить станцию.
        :param code: Код станци.
        :param direction: Направление, удаляемой станции.
        :return: Обновленные данные станции.
        """
        station = await self.__get_station(code, direction)
        if station:

            new_value = (StationsDirection.TO_MOSCOW if station.direction == StationsDirection.FROM_MOSCOW \
                         else StationsDirection.FROM_MOSCOW)

            # TODO Надо оттестить этот момент
            this_station = await self.__get_station(code, new_value)
            if this_station is None:
                self._transport.update_field(
                    collection_name=self._collection_name,
                    field_name="direction",
                    new_value=new_value,
                    instance_id=station.id)
                updated_station = await self.__get_station(code, new_value)
                if updated_station is None:
                    raise DbClientException("Поле не обновилось")
                return updated_station
            else:
                raise ExistException
        else:
            raise NotExistException
