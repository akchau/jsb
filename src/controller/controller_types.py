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

    @staticmethod
    def create_with_direction(data, direction: StationsDirection):
        return Station(**data, direction=direction)

    def to_tuple(self) -> StationInTuple:
        return self.title, self.code


class StationsList(BaseModel):
    stations: list[Station]

    def ext_get_in_list_tuple(self) -> ListStationInTuple:
        return [station.to_tuple() for station in self.stations]

    def int_get_station_by_code(self, code) -> Station | None:
        for station in self.stations:
            if station.code == code:
                return station

    def int_get_not_in(self, station_list: 'StationsList') -> 'StationsList':
        return StationsList(
            stations=[
                station for station in self.stations
                if station not in station_list.stations
            ]
        )


class Schedule(BaseModel):
    arrived_station_code: str
    departure_station_code: str
    schedule: list[tuple]
    update_time: datetime.datetime

