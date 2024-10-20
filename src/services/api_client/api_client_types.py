"""
Модели api-клиента.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StoreType(BaseModel):
    """
    Тип хранилища клиента.
    """
    api_key: str
    base_station_code: str


class ThreadInfo(BaseModel):
    """
    Информация о ветке.
    """
    uid: str


class Schedule(BaseModel):
    """
    Расписание.
    """
    thread: ThreadInfo

    def get_uid(self):
        """
        Получение uid ветки.
        :return:
        """
        return self.thread.uid


class ScheduleFromBaseStation(BaseModel):
    """
    Расписание с базовой станции.
    """
    _schedule_model = Schedule
    schedule: list[_schedule_model]

    def get_thread_uid(self, number_of_thread=0) -> str:
        """
        Получение uid ветки.
        """
        return self.schedule[number_of_thread].get_uid()


class StationInfo(BaseModel):
    """
    Вложенная модель станции.
    """
    code: str
    title: str


class StopInfo(BaseModel):
    """
    Информация о станции.
    """
    station: StationInfo

    def get_info(self):
        """
        Метод парсинга модели StationInfo.
        :return:
        """
        return self.station.dict()


class ThreadData(BaseModel):
    """
    Данные ветки - модель для парсинга API.
    """
    _stop_info_model = StopInfo
    stops: list[_stop_info_model]

    def ext_get_stations(self) -> list[dict]:
        """
        Получений станций наружу после парсинга.
        :return:
        """
        return [
            station.get_info()
            for station in self.stops
        ]


class TransportSubtype(BaseModel):
    title: str
    code: str


class Thread(BaseModel):
    title: str
    short_title: str
    express_type: Optional[str]
    vehicle: Optional[str]
    transport_subtype: TransportSubtype


class Segment(BaseModel):
    thread: Thread
    stops: str
    departure_platform: Optional[str]
    arrival_platform: Optional[str]
    duration: float
    departure: datetime
    arrival: datetime


class ScheduleModel(BaseModel):
    segments: list[Segment]

    def ext(self):
        result = []
        for segment in self.segments:
            result.append((segment.thread.title, segment.arrival, segment.departure,
                           (segment.duration)/60, segment.departure_platform, segment.arrival_platform,
                           segment.stops, segment.thread.transport_subtype.title, segment.thread.transport_subtype.code))
        return result
