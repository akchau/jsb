from src.domain.base import BaseApp
from src.domain.controller_types import DirectionType
from src.domain.utils.send_schedule import DataConstructor
from src.services.db_client.db_client_types import StationDocumentModel


class ScheduleApp(BaseApp):


    async def arrived_station_view(self, update) -> dict:
        departure_station_code, departure_station_direction = await self.parse_data(update)
        available_arrived_stations = [station
             for station in await self._entity.get_all_registered_stations(
                departure_station_direction,
                exclude_direction=True
            )
            if station.code != departure_station_code]
        return {
            "available_arrived_stations": available_arrived_stations,
            "departure_station_direction": departure_station_direction,
            "departure_station_code": departure_station_code
        }

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

    async def schedule_view(self, update):
        departure_station_code, direction, arrived_code = await self.parse_data(update)
        clean_direction = DirectionType(direction=direction)
        schedule = await self._entity.get_schedule(
            departure_station_code=departure_station_code,
            arrived_station_code=arrived_code,
            direction=direction
        )
        departure_station = await self._entity.get_station_by_code(departure_station_code, clean_direction.get_direction())
        arrived_station = await self._entity.get_station_by_code(departure_station_code, clean_direction.get_another())
        return {
            "schedule": DataConstructor(pagination=10).constructor(
                data=schedule.schedule, target_station_one=departure_station.title,
                target_station_two=arrived_station.title),
            "departure_station": departure_station,
            "arrived_station": arrived_station
        }