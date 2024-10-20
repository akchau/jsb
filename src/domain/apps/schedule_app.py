from src.domain.base import BaseApp
from src.domain.utils.send_schedule import DataConstructor
from src.services.db_client.db_client_types import StationDocumentModel


class ScheduleApp(BaseApp):


    async def get_stations(self, direction, for_registration: bool = False) -> list[StationDocumentModel]:
        """
        Выдает контекст на стадии ввода станций
        :param direction: Напарваленеи
        :param for_registration:
        :return:
        """
        if for_registration and direction:
            return [station for station in await self.__schedule_view.get_all_stations_by_api(direction)
                    if station not in await self.__entity.get_all_registered_stations(direction)]
        else:
            return await self.__entity.get_all_registered_stations(direction)

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