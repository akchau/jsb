from src.domain.base import BaseApp
from src.domain.utils.send_schedule import DataConstructor
from src.services.db_client.db_client_types import StationDocumentModel


class ScheduleApp(BaseApp):


    async def arrived_station_view(self, data: tuple[str, str]) -> list[StationDocumentModel]:
        departure_station_code, departure_station_direction = data
        return [station
             for station in await self._entity.get_all_registered_stations(
                departure_station_direction,
                exclude_direction=True
            )
            if station.code != departure_station_code
        ]

    async def departure_station_view(self, data: tuple[str, str] | None) -> list[StationDocumentModel]:
        if data:
            arrived_station_code, direction = data
            stations = [
                station for station in await self._entity.get_all_registered_stations(direction=direction)
                if station.code != arrived_station_code
            ]
        else:
            stations = await self._entity.get_all_registered_stations()
        return stations


    async def get_schedule(self, departure_station_code: str, arrived_station_code: str,
                           direction: str) -> tuple[str, StationDocumentModel, StationDocumentModel]:
        schedule, departure_station, arrived_station = await self.__entity.get_schedule(departure_station_code,
                                                                                       arrived_station_code, direction)
        return DataConstructor.constructor(
            (
                schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            departure_station,
            arrived_station
        )