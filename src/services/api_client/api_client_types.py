from pydantic import BaseModel


class StoreType(BaseModel):
    api_key: str
    base_station_code: str


class ThreadInfo(BaseModel):
    uid: str


class Schedule(BaseModel):
    thread: ThreadInfo

    def get_uid(self):
        return self.thread.uid


class ScheduleFromBaseStation(BaseModel):
    schedule: list[Schedule]

    def get_thread_uid(self, number_of_thread=0) -> str:
        return self.schedule[number_of_thread].get_uid()


class StationInfo(BaseModel):
    code: str
    title: str


class StopInfo(BaseModel):
    station: StationInfo

    def get_info(self):
        return self.station.dict()


class ThreadData(BaseModel):
    stops: list[StopInfo]

    def ext_get_stations(self) -> list[dict]:
        return [
            station.get_info()
            for station in self.stops
        ]