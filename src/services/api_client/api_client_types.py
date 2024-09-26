"""
Модели api-клиента.
"""
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
    schedule: list[Schedule]

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
    stops: list[StopInfo]

    def ext_get_stations(self) -> list[dict]:
        """
        Получений станций наружу после парсинга.
        :return:
        """
        return [
            station.get_info()
            for station in self.stops
        ]
