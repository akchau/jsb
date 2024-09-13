from pydantic import BaseModel


Station = tuple[str, str]
StationsList = list[Station]


class ThreadInfo(BaseModel):
    uid: str


class Schedule(BaseModel):
    thread: ThreadInfo


class ScheduleFromBaseStation(BaseModel):
    schedule: list[Schedule]

    def get_thread_uid(self, number_of_thread=1) -> str:
        return self.schedule[number_of_thread].thread.uid


class StationInfo(BaseModel):
    code: str
    title: str

    def to_tuple(self) -> Station:
        return self.title, self.code


class StopInfo(BaseModel):
    station: StationInfo


class StationsOfThread(BaseModel):
    stops: list[StopInfo]

    def get_stations(self) -> StationsList:
        return [stop.station.to_tuple() for stop in self.stops]
