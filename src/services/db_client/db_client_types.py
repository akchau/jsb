# TODO Эту модель включить в стандартный пакет и обрабатывать. Пока не тестируем
import datetime
import re
from typing import Optional
from pydantic import BaseModel, validator


# TODO Это походу тоже в базовый клиент
class DbClientAuthModel(BaseModel):
    db_name: str
    db_user: str
    db_host: str
    db_password: str
    db_port: int

    @validator('db_name')
    def check_url(cls, v):
        if not re.match(r'^(mongodb|mongodb\+srv)', v):
            raise ValueError('Имя БД должно быть mongodb или mongodb+srv')
        return v


class BaseMongoModel(BaseModel):
    """
    Базовая модель для коллекций с документами с одинаковыми полями.
    """
    id: Optional[str]

    def create_document(self) -> dict:
        current_data = self.dict()
        current_data.pop("id")
        return current_data


class ScheduleDocumentModel(BaseMongoModel):
    """
    Модель документа расписания.
    """
    arrived_station_code: str
    departure_station_code: str
    schedule: list[tuple]
    update_time: datetime.datetime


class StationDocumentModel(BaseMongoModel):
    """
    Модель документа станции.
    """
    code: str
    title: str
    direction: str
