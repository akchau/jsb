import asyncio
import logging
from dataclasses import dataclass
from typing import Type

from src.controller import ScheduleController, controller_types
from src.services.api_client.core import TransportApiClient, ApiInteractor
from src.services.db_client import RegisteredStationsDbClient
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]
    api_interactor_class: Type[ApiInteractor]
    db_client_class: Type[RegisteredStationsDbClient]


@dataclass
class AppDataType:
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient,
    db_client_class=RegisteredStationsDbClient,
    api_interactor_class=ApiInteractor,
)

__api_client = AppDataClasses.api_client_class(
    base_url=settings.API_BASE_URL,
    api_prefix="v3.0",
    store={
        "api_key": settings.API_KEY,
        "base_station_code": settings.BASE_STATION_CODE
    },
    base_connection_timeout=20,
    base_reading_timeout=1000
)

__api_interactor = AppDataClasses.api_interactor_class(__api_client)

__entity = AppDataClasses.db_client_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT
)

__controller = AppDataClasses.controller_class(__api_interactor, __entity)


def get_app_data() -> AppDataType:
    return AppDataType(controller=__controller)


# print(asyncio.run(__api_interactor.get_all_stations_for_base_stations_thread()))
# print(asyncio.run(__entity.register_station(controller_types.Station(code="121212", title="dffdsa", direction=controller_types.StationsDirection.FROM_MOSCOW).dict())))
# print(asyncio.run(__entity.get_all_registered_stations(direction=controller_types.StationsDirection.FROM_MOSCOW)))
# print(asyncio.run(__entity.move_station("121212", controller_types.StationsDirection.FROM_MOSCOW)))
# print(asyncio.run(__entity.get_all_registered_stations(direction=controller_types.StationsDirection.TO_MOSCOW)))
# print(asyncio.run(__entity.register_station(controller_types.Station(code="121212", title="dffdsa", direction=controller_types.StationsDirection.FROM_MOSCOW).dict())))
# print(asyncio.run(__entity.get_all_registered_stations(direction=controller_types.StationsDirection.FROM_MOSCOW)))
# print(asyncio.run(__entity.delete_station("121212")))