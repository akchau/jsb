import asyncio
import datetime
import logging
from dataclasses import dataclass
from typing import Type

from src.controller import ScheduleController, controller_types
from src.controller.controller_types import Schedule
from src.services.api_client.api_client_types import StoreType
from src.services.api_client.core import TransportApiClient, ApiInteractor
from src.services.db_client import RegisteredStationsDbClient
from src.services.db_client.core import ScheduleDbCollection
from src.services.db_client.db_client_types import ScheduleDocumentModel, StationDocumentModel
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]
    api_interactor_class: Type[ApiInteractor]
    stations_db_client_class: Type[RegisteredStationsDbClient]
    schedule_db_client_class: Type[ScheduleDbCollection]


@dataclass
class AppDataType:
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient,
    stations_db_client_class=RegisteredStationsDbClient,
    api_interactor_class=ApiInteractor,
    schedule_db_client_class=ScheduleDbCollection
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
    dp_port=settings.DB_PORT,
    collection_model=StationDocumentModel
)

__schedule_entity = AppDataClasses.schedule_db_client_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT,
    collection_model=ScheduleDocumentModel
)

__controller = AppDataClasses.controller_class(__api_interactor, __stations_entity, __schedule_entity)


def get_app_data() -> AppDataType:
    return AppDataType(controller=__controller)


async def main():
    await __schedule_entity.write_schedule(new_object=Schedule(arrived_station_code="123",
                                                               departure_station_code="124",
                                                               update_time=datetime.datetime.now(),
                                                               schedule=[("station_1", "djeklfw",)]))
    print(await __schedule_entity.get_schedule(departure_station_code="124", arrived_station_code="123"))

asyncio.run(main())
