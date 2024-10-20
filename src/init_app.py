"""
Главный модуль инициализации приложения.
"""
import logging
from dataclasses import dataclass
from typing import Type

from telegram.ext import Application
from telegram.ext._applicationbuilder import BuilderType


from src.domain import ScheduleController
from src.domain.core import AdminController
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    """
    Класс для сбрки классов приложения.
    """
    schedule_controller_class: Type[ScheduleController]
    application_builder_class: Type[Application]
    admin_controller_class: Type[AdminController]


@dataclass
class AppDataType:
    """
    Класс с объектами классов приложения.
    """
    schedule_controller: ScheduleController
    admin_controller: AdminController
    application_builder: BuilderType


AppDataClasses = AppDataClassesType(
    schedule_controller_class=ScheduleController,
    application_builder_class=Application,
    admin_controller_class=AdminController
)


__schedule_controller = AppDataClasses.schedule_controller_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    db_port=settings.DB_PORT,
    pagination=settings.PAGINATION
)

__admin_controller = AppDataClasses.admin_controller_class(
    base_url=settings.API_BASE_URL,
    api_key=settings.API_KEY,
    base_station_code=settings.BASE_STATION_CODE,
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    db_port=settings.DB_PORT,
)

__application_builder = AppDataClasses.application_builder_class.builder().token(settings.BOT_TOKEN)


def get_app_data() -> AppDataType:
    """
    Функция вернет все объекты приложения.
    :return: Объекты приложения.
    """
    return AppDataType(schedule_controller=__schedule_controller,
                       application_builder=__application_builder,
                       admin_controller=__admin_controller)
