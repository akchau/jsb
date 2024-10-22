# Взаимодействие с api на верхнем уровне
from typing import TypeVar, Generic, Type

from api_client import RequestException
from pydantic import ValidationError

from src.domain.controller_types import StationsDirection, SchedulesBetweenStations
from src.domain.exc import InternalError
from src.services.api_client import ScheduleFromBaseStation, ThreadData, TransportApiClient
from src.services.api_client.api_client_types import ScheduleResponse



def base_error_handler(func):

    """
    Декоратор обработает ошибки при работе с api
    Глобальная ошибка которую выбрасывает транспорт -> Внутренняя ошибка.
    Ошибка при парсинге модели ответа -> Внутренняя ошибка.
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            raise InternalError(f"Ошибка при запросе к api {str(e)}")
        except ValidationError as e:
            raise InternalError(f"Ошибка валидации ответа API {str(e)}")
    return wrapper




ItemModel = TypeVar("ItemModel")


class Parser(Generic[ItemModel]):

    @staticmethod
    def parse_to_data_model(model: Type[ItemModel], data = None, **kwargs) -> ItemModel | list[ItemModel]:
        try:
            if isinstance(data, list):
                return [model(**item, **kwargs) for item in data]
            elif isinstance(data, dict):
                return model(**data, **kwargs)
            elif data is None:
                return model(**kwargs)
        except ValidationError as e:
            raise InternalError(f"Ошибка при парсинге данных {data} API в модель {model}: {str(e)}")


#  Модели в которые парсится ответ Api
StationModel = TypeVar("StationModel")
ScheduleModel = TypeVar("ScheduleModel")


class ApiView(Generic[StationModel, ScheduleModel]):
    """
    Драйвер контроллера для взаимодействия с сервисом api
    """

    def __init__(self, transport: TransportApiClient, station_model: Type[StationModel],
                 schedule_model: Type[ScheduleModel]):
        self.__api_client = transport # Готовый к использованию транспорт.
        self.__station_model = station_model  # Модель Станции
        self.__schedule_model = schedule_model  # Модель расписания
        self.__parser = Parser

    @base_error_handler
    async def get_all_stations_by_api(self, direction: StationsDirection) -> list[StationModel]:
        """
        Получение списка станций.
        :param direction: Направление.
        :return: Список станций.
        """
        branch: ScheduleFromBaseStation = await self.__api_client.get_branch_info()
        thread: ThreadData = await self.__api_client.get_thread_info(branch.get_thread_uid())
        return self.__parser.parse_to_data_model(model=self.__station_model, direction=direction,
                                                 data=thread.ext_get_stations())

    async def get_station_by_api(self, direction: StationsDirection, code: str) -> StationModel | None:
        stations: list[StationModel] = await self.get_all_stations_by_api(direction)
        for station in stations:
            if station.code == code:
                return station

    @base_error_handler
    async def get_schedule(self, departure_station_code: str, arrived_station_code: str) -> SchedulesBetweenStations:
        direct_schedule: ScheduleResponse = await self.__api_client.get_schedule(
            departure_station_code, arrived_station_code)
        back_schedule: ScheduleResponse = await self.__api_client.get_schedule(
            arrived_station_code, departure_station_code)
        return self.__parser.parse_to_data_model(
            model=SchedulesBetweenStations,
            departure_station_code=departure_station_code,
            arrived_station_code=arrived_station_code,
            schedules=(self.__parser.parse_to_data_model(direct_schedule.ext()),
                       self.__parser.parse_to_data_model(back_schedule.ext()))
        )
