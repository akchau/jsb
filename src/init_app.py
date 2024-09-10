import logging
from dataclasses import dataclass
from typing import Type

from src.controller.core import ScheduleController
from src.services.api_client.core import TransportApiClient
from src.services.db_client.core import DbClient
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]
    db_client_class: Type[DbClient]


@dataclass
class AppDataType:
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient,
    db_client_class=DbClient
)

__api_client = AppDataClasses.api_client_class(
    base_url=settings.API_BASE_URL,
    api_prefix="v3.0",
    store={
        "api_key": settings.API_KEY,
        "base_station_code": settings.BASE_STATION_CODE
    })
__entity = AppDataClasses.db_client_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT,
)
__controller = AppDataClasses.controller_class(__api_client, __entity)


def get_app_data() -> AppDataType:
    return AppDataType(controller=__controller)
