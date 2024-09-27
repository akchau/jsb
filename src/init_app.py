"""
Главный модуль инициализации приложения.
"""
import asyncio
import datetime
import logging
from dataclasses import dataclass
from typing import Type

from src.controller import ScheduleController
from src.controller.controller_types import Station, StationsDirection, Schedule
from src.services.api_client.api_client_types import StoreType
from src.services.api_client.core import TransportApiClient, ApiInteractor
from src.services.db_client.core import ScheduleEntity
from src.services.db_client.db_client_types import ScheduleDocumentModel, StationDocumentModel
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    """
    Класс для сбрки классов приложения.
    """
    controller_class: Type[ScheduleController]
    api_client_class: Type[TransportApiClient]
    api_interactor_class: Type[ApiInteractor]
    entity_class: Type[ScheduleEntity]


@dataclass
class AppDataType:
    """
    Класс с объектами классов приложения.
    """
    controller: ScheduleController


AppDataClasses = AppDataClassesType(
    controller_class=ScheduleController,
    api_client_class=TransportApiClient,
    api_interactor_class=ApiInteractor,
    entity_class=ScheduleEntity
)

__api_client = AppDataClasses.api_client_class(
    base_url=settings.API_BASE_URL,
    api_prefix="v3.0",
    store=StoreType(api_key=settings.API_KEY, base_station_code=settings.BASE_STATION_CODE)
)

__api_interactor = AppDataClasses.api_interactor_class(__api_client)

__entity = AppDataClasses.entity_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    dp_port=settings.DB_PORT,
    station_domain_model=Station
)
__entity.set_on_station_change(callback=lambda x: None)

__controller = AppDataClasses.controller_class(__api_interactor, __entity)


def get_app_data() -> AppDataType:
    """
    Функция вернет все объекты приложения.
    :return: Объекты приложения.
    """
    return AppDataType(controller=__controller)


async def main():
    """
    Мануальное тестирование.
    :return:
    """
    await __entity.collections.schedule.write_schedule(new_schedule=ScheduleDocumentModel(arrived_station_code="123",
                                                       departure_station_code="124",
                                                       update_time=datetime.datetime.now(),
                                                       schedule=[("station_1", "djeklfw")]))
    schedule = await __entity.collections.schedule.write_schedule(
        new_schedule=ScheduleDocumentModel(
            arrived_station_code="124",
            departure_station_code="123",
            update_time=datetime.datetime.now(),
            schedule=[("station_2", "djeklfw")]
        )
    )
    await __entity.collections.schedule.delete_schedule(schedule)
    print(await __entity.collections.schedule.get_schedule(departure_station_code="124", arrived_station_code="123"))
    # ------------------------------------------------------------------------------------------------------------------
    await __entity.collections.stations.register_station(
        new_station=StationDocumentModel(
            direction=StationsDirection.FROM_MOSCOW,
            code="123",
            title="ЖЕЛДОР"
        )
    )
    print(await __entity.collections.stations.get_all_registered_stations())
    print(await __entity.collections.stations.get_all_registered_stations(direction=StationsDirection.TO_MOSCOW))
    await __entity.collections.stations.move_station(code="123", direction=StationsDirection.FROM_MOSCOW)
    await __entity.collections.stations.delete_station(code="123", direction=StationsDirection.TO_MOSCOW)
    # ------------------------------------------------------------------------------------------------------------------
    print(await __entity.get_all_registered_stations())
    await __entity.register_station(
        station=Station(
            direction=StationsDirection.FROM_MOSCOW,
            code="123",
            title="ЖЕЛДОР"
        )
    )
    await __entity.write_schedule(
        new_object=Schedule(
            arrived_station_code="123",
            departure_station_code="124",
            update_time=datetime.datetime.now(),
            schedule=[("station_1", "djeklfw")]
        )
    )
    print(await __entity.get_schedule(arrived_station_code="123", departure_station_code="124"), "Связанное расписание")
    print(await __entity.get_all_registered_stations())
    await __entity.move_station(code="123", direction=StationsDirection.FROM_MOSCOW)
    await __entity.delete_station(direction=StationsDirection.TO_MOSCOW, code="123")
    print(await __entity.get_all_registered_stations())

asyncio.run(main())
