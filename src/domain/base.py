from src.domain.controller_types import Station, Schedule, DirectionType, StationsDirection, StationActionEnum
from src.domain.exc import InternalError
from src.domain.send_schedule import DataConstructor
from src.services import ScheduleEntity, ApiInteractor, ApiError, DbClientException


class BaseController:

    def __init__(self, base_url: str, api_key: str, base_station_code: str, pagination: int, **kwargs):
        self._station_model = Station
        self._entity = ScheduleEntity.construct(**kwargs, station_domain_model=self._station_model)
        self._api = ApiInteractor(base_url, api_key, base_station_code)
        self._api_error = ApiError
        self._internal_error = InternalError
        self._db_client_error = DbClientException
        self._schedule_model = Schedule
        self._direction_validator = DirectionType
        self._station_direction = StationsDirection
        self._action_enum = StationActionEnum
        self._schedule_constructor = DataConstructor(pagination)
