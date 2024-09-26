import datetime
from enum import Enum
from pydantic import BaseModel


class StationsDirection(str, Enum):
    """
    Направления для регистрации станций.
    """
    TO_MOSCOW = "TO_MOSCOW"
    FROM_MOSCOW = "FROM_MOSCOW"


StationInTuple = tuple[str, str]
ListStationInTuple = list[StationInTuple]


class Station(BaseModel):
    code: str
    title: str
    direction: StationsDirection


    def to_tuple(self) -> StationInTuple:
        return self.title, self.code

    def __eq__(self, other: 'Station') -> bool:
        return self.code == other.code and self.direction == other.direction


class Schedule(BaseModel):
    arrived_station_code: str
    departure_station_code: str
    schedule: list[tuple]
    update_time: datetime.datetime

    #TODO c помощью root validator проверить поля уникальны

