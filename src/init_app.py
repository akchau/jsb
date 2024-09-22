import asyncio
import logging
from dataclasses import dataclass
from typing import Type

from src.controller import ScheduleController, controller_types
from src.services.api_client.api_client_types import StoreType
from src.services.api_client.core import TransportApiClient, ApiInteractor
from src.services.db_client import RegisteredStationsDbClient
from src.services.db_client.core import ScheduleDbClient
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]
    api_interactor_class: Type[ApiInteractor]
    stations_db_client_class: Type[RegisteredStationsDbClient]
    schedule_db_client_class: Type[ScheduleDbClient]


@dataclass
class AppDataType:
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient,
    stations_db_client_class=RegisteredStationsDbClient,
    api_interactor_class=ApiInteractor,
    schedule_db_client_class=ScheduleDbClient
)

__api_client = AppDataClasses.api_client_class(
    base_url=settings.API_BASE_URL,
    api_prefix="v3.0",
    store=StoreType(api_key=settings.API_KEY, base_station_code=settings.BASE_STATION_CODE)
)

__api_interactor = AppDataClasses.api_interactor_class(__api_client)

__stations_entity = AppDataClasses.stations_db_client_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT
)

__schedule_entity = AppDataClasses.schedule_db_client_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT
)

__controller = AppDataClasses.controller_class(__api_interactor, __stations_entity)


def get_app_data() -> AppDataType:
    return AppDataType(controller=__controller)



# async def main():
#     await __schedule_entity.write_schedule(departure_station_code="123", arrived_station_code="21231",
#                                            schedule_data=[("ras", "ras")])
#     print(await __schedule_entity.get_schedule(departure_station_code="123", arrived_station_code="21231"))
#
# asyncio.run(main())
