"""
Модуль обработчиков расписания
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.handlers.data_handler import parse_data, create_data

from src.init_app import get_app_data


async def departure_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    data = await parse_data(update)

    if data:
        arrived_code, direction = data
        stations, _ = await get_app_data().controller.get_stations(direction=direction)
        station_buttons = [[InlineKeyboardButton(text=station.title,
                                                 callback_data=await create_data(
                                                    SCHEDULE_VIEW,
                                                    station.code, station.direction, arrived_code))]
                           for station in stations]
    else:
        stations = await get_app_data().controller.get_stations()
        station_buttons = [[InlineKeyboardButton(text=station.title,
                                                 callback_data=await create_data(
                                                     ARRIVED_STATION,
                                                     station.code, station.direction))]
                           for station in stations]
    buttons = [
        *station_buttons,
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.departure_station.title, reply_markup=keyboard)
    return DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """

    code, direction = await parse_data(update)
    stations = await get_app_data().controller.get_stations(direction, exclude_direction=True)
    buttons = [
        *[[InlineKeyboardButton(
            text=station.title,
            callback_data=await create_data(SCHEDULE_VIEW, code, direction, station.code)
        )] for station in stations],
        [
            InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                                 callback_data=str(MAIN_MENU)),
            InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                                 callback_data=str(DEPARTURE_STATION))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.arrived_station.title, reply_markup=keyboard)
    return ARRIVED_STATION


async def schedule_view(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    departure_code, direction, arrived_code = await parse_data(update)
    schedule: list[str] = await get_app_data().controller.get_schedule(departure_code, arrived_code)

    if update.callback_query:
        await update.callback_query.message.delete()

    buttons = [
        [InlineKeyboardButton(text=MenuSections.arrived_station.back_to_title,
                              callback_data=await create_data(str(ARRIVED_STATION),
                                                              departure_code, direction)),
         InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                              callback_data=await create_data(str(DEPARTURE_STATION),
                                                              arrived_code, direction))],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                              callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    for time in schedule:
        await update.effective_message.reply_text(time)
    await update.effective_message.reply_text(f"Расписание", reply_markup=keyboard)
    return SCHEDULE_VIEW
