import logging
from dataclasses import dataclass
from typing import Type

from src.controller.core import ScheduleController
from src.services.api_client.core import TransportApiClient
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]


@dataclass
class AppDataType:
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient
)

__api_client = TransportApiClient(base_url=settings.API_BASE_URL, api_prefix="v3.0",
                                  store={"api_key": settings.API_KEY})
__controller = ScheduleController(__api_client)


def get_app_data() -> AppDataType:
    return AppDataType(controller=__controller)


print(__api_client.get_schedule_from_station())
