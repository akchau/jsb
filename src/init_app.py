"""
Главный модуль инициализации приложения.
"""
import logging
from dataclasses import dataclass
from typing import Type

from telegram.ext import Application
from telegram.ext._applicationbuilder import BuilderType

from src.domain import Controller
from src.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class AppDataClassesType:
    """
    Класс для сбрки классов приложения.
    """
    controller_class: Type[Controller]
    application_builder_class: Type[Application]


@dataclass
class AppDataType:
    """
    Класс с объектами классов приложения.
    """
    controller: Controller
    application_builder: BuilderType


AppDataClasses = AppDataClassesType(
    controller_class=Controller,
    application_builder_class=Application,
)


__controller = AppDataClasses.controller_class(
    db_name=settings.DB_NAME,
    db_user=settings.DB_USER,
    db_host=settings.DB_HOST,
    db_password=settings.DB_PASSWORD,
    db_port=settings.DB_PORT,
    pagination=settings.PAGINATION,
    base_url=settings.API_BASE_URL,
    api_key=settings.API_KEY,
    base_station_code=settings.BASE_STATION_CODE
)

__application_builder = AppDataClasses.application_builder_class.builder().token(settings.BOT_TOKEN)


def get_app_data() -> AppDataType:
    """
    Функция вернет все объекты приложения.
    :return: Объекты приложения.
    """
    return AppDataType(controller=__controller,
                       application_builder=__application_builder)
