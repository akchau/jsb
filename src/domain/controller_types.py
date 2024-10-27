"""
Типы контроллера
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, validator

from src.services.db_client.db_client_types import ScheduleDocumentModel


class StationActionEnum(str, Enum):
    DELETE = "DELETE"
    MOVE = "MOVE"
    REGISTER = "REGISTER"


class StationsDirection(str, Enum):
    """
    Направления для регистрации станций.
    """
    TO_MOSCOW = "TO_MOSCOW"
    FROM_MOSCOW = "FROM_MOSCOW"


class DirectionType(BaseModel):
    """
    Валидатор для направления.
    """
    direction: str

    def get_tuple(self) -> tuple[str, StationsDirection]:
        return self.get_text_direction(), self.get_direction()

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
            return StationsDirection.TO_MOSCOW
        elif self.direction == StationsDirection.TO_MOSCOW:
            return StationsDirection.FROM_MOSCOW
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



class AppsEnum(str, Enum):
    ADMIN = "ADMIN"
    SCHEDULE = "SCHEDULE"


class MenuSection(BaseModel):
    title: str
    back_to_title: Optional[str] = "Неизвестное значение"


class MenuSections:
    main_menu = MenuSection(title='Главное меню 🔢', back_to_title='⬅️ Главное меню 🔢')
    admin_zone = MenuSection(title='Админка 🔴️️', back_to_title='⬅️ Главное меню администартора 🔴️️')
    schedule = MenuSection(title="Расписание 📅", back_to_title="⬅️ Расписание 📅")
    my_stations = MenuSection(title="Мои станции 🛤", back_to_title="️⬅️ к выбору направления")
    departure_station = MenuSection(title="Станция отправления", back_to_title="🔁 станцию отправления")
    arrived_station = MenuSection(title="Станция прибытия", back_to_title="🔁 станцию прибытия")
    register_station = MenuSection(title="Новая станция 🆕", back_to_title="️⬅️ к выбору направления")
    delete = MenuSection(title="Удалить ❌")
    move = MenuSection(title="Переместить 🔁")
    register_station_with_direction_to_moscow = MenuSection(title="В Москву 🏢🚄🏡",
                                                              back_to_title="Зарегистрировать 🆕")
    register_station_with_direction_from_moscow = MenuSection(title="Из Москвы 🏡🚄🏢",
                                                              back_to_title="Зарегистрировать 🆕")
    registered_station_with_direction_to_moscow = MenuSection(title="В Москву 🏢🚄🏡",
                                                            back_to_title="Мои станции 🛤")
    registered_station_with_direction_from_moscow = MenuSection(title="Из Москвы 🏡🚄🏢",
                                                              back_to_title="Мои станции 🛤")


