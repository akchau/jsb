"""
Типы контроллера
"""
import datetime
from enum import Enum
from pydantic import BaseModel, validator, root_validator

from src.services.db_client.db_client_types import ScheduleDocumentModel


class StationsDirection(str, Enum):
    """
    Направления для регистрации станций.
    """
    TO_MOSCOW = "TO_MOSCOW"
    FROM_MOSCOW = "FROM_MOSCOW"


class StationActionEnum(str, Enum):
    DELETE = "DELETE"
    MOVE = "MOVE"
    REGISTER = "REGISTER"


StationInTuple = tuple[str, str]
ListStationInTuple = list[StationInTuple]


class Schedule(BaseModel):
    """
    Расписание
    """
    arrived_station_code: str
    departure_station_code: str
    schedule: list[tuple]
    update_time: datetime.datetime

    @root_validator
    def check_stations(cls, values: dict) -> dict:
        """
        Проверка кодов.
        :param values: Значения полей моделей.
        :return:
        """
        arrived_station_code = values.get('arrived_station_code')
        departure_station_code = values.get('departure_station_code')
        if arrived_station_code == departure_station_code:
            raise ValueError('Коды должны отличаться')
        return values


class DirectionType(BaseModel):
    """
    Валидатор для направления.
    """

    direction: str

    def get_text_direction(self) -> str:
        """
        Представление направления строкой для бота.
        :return: Направление.
        """
        if self.direction == StationsDirection.FROM_MOSCOW:
            return "Из Москвы 🏡🚄🏢"
        elif self.direction == StationsDirection.TO_MOSCOW:
            return "В Москву 🏢🚄🏡"
        else:
            raise ValueError("Ошибка напрвления")

    def get_direction(self) -> StationsDirection:
        """
        Представление направления строкой для бота.
        :return: Направление.
        """
        if self.direction == StationsDirection.FROM_MOSCOW:
            return StationsDirection.FROM_MOSCOW
        elif self.direction == StationsDirection.TO_MOSCOW:
            return StationsDirection.TO_MOSCOW
        else:
            raise ValueError("Ошибка напрвления")

    def get_another(self) -> StationsDirection:
        """
        Представление направления строкой для бота.
        :return: Направление.
        """
        if self.direction == StationsDirection.FROM_MOSCOW:
            return StationsDirection.FROM_MOSCOW
        elif self.direction == StationsDirection.TO_MOSCOW:
            return StationsDirection.TO_MOSCOW
        else:
            raise ValueError("Ошибка напрвления")

    @validator("direction")
    def clean_direction(cls, v: str) -> str:
        """
        Валидатор для направления.
        :param v: Направление.
        :return: Валидное напрвление.
        """
        if v not in StationsDirection.__members__:
            raise ValueError("Ошибка напрвления")
        return v



class SchedulesBetweenStations(BaseModel):
    departure_station_code: str
    arrived_station_code: str
    schedules: tuple[ScheduleDocumentModel, ScheduleDocumentModel]
