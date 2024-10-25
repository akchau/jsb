from src.domain.base import BaseApp, app_handler
from src.domain.controller_types import DirectionType
from src.domain.utils.send_schedule import DataConstructor
from src.services.db_client.db_client_types import StationDocumentModel


class ScheduleApp(BaseApp):

    @app_handler
    async def arrived_station_view(self, user, data) -> dict:
        departure_station_code, departure_station_direction = data

        available_arrived_stations = [
            station
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

    @app_handler
    async def departure_station_view(self, user, data) -> dict:
        arrived_station_already_choice = True if data else None
        if arrived_station_already_choice:
            clean_direction = DirectionType(direction=data["arrived_station_direction"])
            available_departure_stations = [
                station for station in await self._entity.get_all_registered_stations(direction=clean_direction)
                if station.code != data["arrived_station_code"]
            ]
        else:
            available_departure_stations = await self._entity.get_all_registered_stations()
        available_departure_stations_buttons = []
        for departure_station_item in available_departure_stations:
            available_departure_stations_buttons.append(
                {
                    "departure_station_title": departure_station_item.title,
                    "departure_stations_buttons": await self._context_creator.create_data(
                        {
                            "departure_station_code": departure_station_item.code,
                            "departure_station_direction": departure_station_item.direction,
                            "arrived_station_code": data["arrived_station_code"]
                        }
                    )
                }
            )
        return {
            "available_departure_stations_buttons": available_departure_stations_buttons,
            "message": "Выберите станцию отпарвления"
        }

    @app_handler
    async def schedule_view(self, user, data):
        departure_station_code, direction, arrived_code = data
        clean_direction = DirectionType(direction=direction)

        schedule = await self._entity.get_schedule(
            departure_station_code=departure_station_code,
            arrived_station_code=arrived_code,
            direction=direction
        )
        departure_station = await self._entity.get_station_by_code(
            departure_station_code,
            clean_direction.get_direction()
        )
        arrived_station = await self._entity.get_station_by_code(
            departure_station_code,
            clean_direction.get_another()
        )

        return {
            "schedule": DataConstructor(pagination=10).constructor(
                data=schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            "change_arrived_station_button": (
                arrived_station.title,
                await self._context_creator.create_data(
                    {
                        "direction": clean_direction.get_direction(),
                        "code": departure_station.code
                    }
                )
            ),
            "change_departure_station_button": (
                departure_station.title,
                await self._context_creator.create_data(
                    {
                        "direction": clean_direction.get_direction(),
                        "code": departure_station.code
                    }
                )
            )

            "message": f"Расписание {departure_station.title} - {arrived_station.title}"
        }