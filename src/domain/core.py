"""
Главный модуль контроллера.
"""
import logging
from dataclasses import dataclass
from typing import Type

from src.domain.utils.api_view import ApiView
from src.services import ScheduleEntity
from .apps.admin_app import AdminApp
from .apps.schedule_app import ScheduleApp
from .base import BaseApp
from ..services.api_client.api_client_types import StoreType
from ..services.api_client.core import TransportApiClient
from ..services.db_client.db_client_types import StationDocumentModel, ScheduleDocumentModel

logger = logging.getLogger(__name__)


class Controller:

    def __init__(self, pagination: int, base_url: str, api_key: str, base_station_code: str, **kwargs):
        self.__entity = ScheduleEntity.construct(**kwargs)
        self.__api_transport = TransportApiClient(
            base_url=base_url,
            api_prefix="v3.0",
            store=StoreType(
                api_key=api_key,
                base_station_code=base_station_code
            ),
            time_sleep=1,
            iterations=3
        )
        self.__view = ApiView(self.__api_transport,
                              station_model=StationDocumentModel, schedule_model=ScheduleDocumentModel)

        @dataclass
        class Apps:
            schedule: Type[BaseApp]
            admin: Type[AdminApp]

            def get_app(self, name: str) -> BaseApp:
                return getattr(self, name)

        self.__apps = Apps(
            schedule=ScheduleApp,
            admin=AdminApp
        )


        class Services

    def app(self, app: str):
        return getattr(self.__apps, app)
