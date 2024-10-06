"""
Меню при регистрации станции.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.handlers.data_handler import parse_data, create_data

from src.init_app import get_app_data


async def registered_stations(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню регистрации станции.
    :param update:
    :param _:
    :return:
    """
    directions = await get_app_data().controller.get_directions()
    buttons = [
        [
            InlineKeyboardButton(
                text="Из Москвы 🏡🚄🏢",
                callback_data= await create_data(REGISTERED_STATIONS_WITH_DIRECTION,
                                                 directions.FROM_MOSCOW)
            ),
            InlineKeyboardButton(
                text="В Москву 🏢🚄🏡",
                callback_data=await create_data(REGISTERED_STATIONS_WITH_DIRECTION,
                                                directions.TO_MOSCOW)
            ),
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=MenuSections.my_stations.title, reply_markup=keyboard)
    return REGISTERED_STATIONS


async def registered_stations_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    parsed_data = await parse_data(update)
    if len(parsed_data) == 3:
        direction, action, code = parsed_data
        await get_app_data().controller.station_action(direction=direction, code=code, action=action)
    else:
        direction = parsed_data
    print(direction)
    stations, text_direction = await get_app_data().controller.get_stations(direction=direction)
    print(stations, text_direction)
    buttons = [
        *[
            [
                InlineKeyboardButton(
                    station.title,
                    callback_data= await create_data(EDIT_STATION,
                                                     direction, station.code)
                )
            ] for station in stations
        ],
        [
            InlineKeyboardButton(text=MenuSections.my_stations.back_to_title,
                                 callback_data=str(REGISTERED_STATIONS)),
            InlineKeyboardButton(text=MenuSections.register_station_with_direction_from_moscow.back_to_title,
                                 callback_data=await create_data(REGISTER_STATION_WITH_DIRECTION,
                                                                 direction))

        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    print(keyboard, text_direction)
    await update.callback_query.edit_message_text(
        text=f"{MenuSections.my_stations.title}\nНаправление: {text_direction}",
        reply_markup=keyboard)
    return REGISTERED_STATIONS_WITH_DIRECTION
