import logging
from enum import Enum

from src.domain.base import BaseApp, DataHandler
from src.domain.controller_types import DirectionType, MenuSections
from src.domain.utils.send_schedule import DataConstructor


logger = logging.getLogger(__name__)


class DataKeysEnum(str, Enum):
    departure_station_direction = "departure_station_direction"
    departure_station_code = "departure_station_code"
    arrived_station_code = "arrived_station_code"


class ScheduleApp(BaseApp):


    async def arrived_station_view(self, update) -> dict:
        """
        Обработичк для получения списка станций прибытия.
        :param user: username.
        :param data: Контектст.
        :return: Данные для рендера сообщения.
        """
        context = await DataHandler().get_context(update)
        user = context.user
        data = context.data
        departure_station_code = data["dep_st"]
        departure_station_direction = data["dep_st_dir"]
        logger.debug(f"Пользователь {user.username} выбирает станцию прибытия.")
        available_arrived_stations = [station for station in await self._entity.get_all_registered_stations(
            direction=departure_station_direction,
            exclude_direction=True
        ) if station.code != departure_station_code]
        available_arrived_stations_buttons = []
        for arrived_station_item in available_arrived_stations:
            available_arrived_stations_buttons.append(
                (
                    arrived_station_item.title,
                    await self._context_creator.create_data(
                        {
                            **data,
                            "arr_st": arrived_station_item.code
                        }
                    )
                )
            )

        return {
            "available_arrived_stations_buttons": available_arrived_stations_buttons,
            "message": "Выберите станцию прибытия.",
            "back_to_menu_title": MenuSections.main_menu.back_to_title,
            "back_to_departure_station_button": MenuSections.departure_station.back_to_title
        }

    async def departure_station_view(self, update) -> dict:
        """
        Обработичк для получения списка станций отправления.
        :param user: username.
        :param data: Контектст.
        :return: Данные для рендера сообщения.
        """
        context = await DataHandler().get_context(update)
        user = context.user
        data = context.data
        arrived_station_already_choice = True if data else None

        if arrived_station_already_choice:
            # При смене станции.
            logger.debug(f"Пользователь {user.username} меняет станцию отправления.")
            arrived_station_direction = data["arr_st_dir"]
            arrived_station_code = data["arr_st"]
            clean_arrived_station_direction = DirectionType(direction=arrived_station_direction)
            available_departure_stations = [
                station for station in await self._entity.get_all_registered_stations(
                    direction=clean_arrived_station_direction.get_another()
                )
                if station.code != arrived_station_code
            ]
            available_departure_stations_buttons: list[tuple[str, str]] = [
                (
                    departure_station_item.title,
                    await self._context_creator.create_data(
                        {
                            "dep_st": departure_station_item.code,
                            "dep_st_dir": departure_station_item.direction,
                            "arr_st": arrived_station_code
                        }
                    )
                ) for departure_station_item in available_departure_stations
            ]
        else:
            # При первом заходе.
            logger.debug(f"Пользователь {user.username} выбирает станцию отправления.")
            available_departure_stations_buttons: list[tuple[str, str]] = [
                (
                    departure_station_item.title,
                    await self._context_creator.create_data(
                        {
                            "dep_st": departure_station_item.code,
                            "dep_st_dir": departure_station_item.direction,
                        }
                    )
                ) for departure_station_item in await self._entity.get_all_registered_stations()
            ]
        return {
            "available_departure_stations_buttons": available_departure_stations_buttons,
            "message": "Выберите станцию отпарвления.",
            "redirect_to_schedule": arrived_station_already_choice,
            "back_to_main_menu_button_title": MenuSections.main_menu.back_to_title
        }

    async def schedule_view(self, update) -> dict:
        context = await DataHandler().get_context(update)
        user = context.user
        data = context.data
        departure_station_direction = data["dep_st_dir"]
        departure_station_code = data["dep_st"]
        arrived_station_code = data["arr_st"]
        clean_direction = DirectionType(direction=departure_station_direction)
        logger.debug(f"Пользователь {user.username} получает расписание между {departure_station_code} - "
                     f"{arrived_station_code}")
        schedule = await self._entity.get_schedule(
            departure_station_code=departure_station_code,
            arrived_station_code=arrived_station_code,
            direction=departure_station_direction
        )
        departure_station = await self._entity.get_station_by_code(
            code=departure_station_code,
            direction=clean_direction.get_direction()
        )
        arrived_station = await self._entity.get_station_by_code(
            code=arrived_station_code,
            direction=clean_direction.get_another()
        )
        return {
            "schedule": DataConstructor(pagination=10).constructor(
                data=schedule.schedule,
                target_station_one=departure_station.title,
                target_station_two=arrived_station.title
            ),
            "change_arrived_station_button": (
                "Сменть станцию прибытия",
                await self._context_creator.create_data(
                    {
                        "dep_st": clean_direction.get_direction(),
                        "dep_st_dir": departure_station.code
                    }
                )
            ),
            "change_departure_station_button": (
                "Сменть станцию отправления",
                await self._context_creator.create_data(
                    {
                        "arr_st_dir": clean_direction.get_direction(),
                        "arr_st": arrived_station.code,
                    }
                )
            ),
            "message": f"Расписание {departure_station.title} - {arrived_station.title}",
            "back_to_menu_title": MenuSections.main_menu.back_to_title
        }