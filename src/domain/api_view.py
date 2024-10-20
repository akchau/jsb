from typing import TypeVar, Generic

from api_client import RequestException
from pydantic import ValidationError

from src.domain.controller_types import StationsDirection
from src.domain.exc import InternalError
from src.services.api_client import ScheduleFromBaseStation, ThreadData, TransportApiClient


StationModel = TypeVar("StationModel")
ScheduleModel = TypeVar("ScheduleModel")


class ApiView(Generic[StationModel, ScheduleModel]):

    def __init__(self, transport: TransportApiClient, station_model: StationModel, schedule_model: ScheduleModel):
        self.__api_client = transport
        self._api_error = RequestException
        self._validation_error = ValidationError
        self._internal_error = InternalError
        self._station_model = station_model
        self._schedule_model = schedule_model

    async def get_all_stations_by_api(self, direction: StationsDirection) -> list[StationModel]:
        try:
            branch: ScheduleFromBaseStation = await self.__api_client.get_branch_info()
            thread: ThreadData = await self.__api_client.get_thread_info(branch.get_thread_uid())
        except self._api_error as e:
            raise self._internal_error(str(e))
        except ValidationError as e:
            raise self._internal_error(f"Ошибка валидации ответа API {str(e)}")
        return [self._station_model(**station, direction=direction) for station in thread.ext_get_stations()]

    async def get_station_by_api(self, direction: StationsDirection, code: str) -> StationModel | None:
        stations: list[StationModel] = await self.get_all_stations_by_api(direction)
        for station in stations:
            if station.code == code:
                return station

    async def get_schedule(self, departure_station_code: str, arrived_station_code: str) -> ScheduleModel:
        try:
            direct_schedule = await self.__api_client.get_schedule(departure_station_code, arrived_station_code)
            back_schedule = await self.__api_client.get_schedule(arrived_station_code, departure_station_code)
            return (self._schedule_model.parse_obj(direct_schedule.ext()),
                    self._schedule_model.parse_obj(back_schedule.ext()))
        except RequestException as e:
            raise self._internal_error(str(e))
        except ValidationError as e:
            raise self._internal_error(f"Ошибка валидации ответа API {str(e)}")
