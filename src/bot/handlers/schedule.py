"""
Модуль обработчиков расписания
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.bot.bot_types import MenuSections
from src.bot.handlers.data_handler import parse_data, create_data

from src.controller.controller_types import Station
from src.init_app import get_app_data


async def departure_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    stations: list[Station] = await get_app_data().controller.get_stations()
    buttons = [
        *[[InlineKeyboardButton(text=station.title,
                                callback_data=await create_data(constants.ARRIVED_STATION,
                                                                station.code, station.direction))]
          for station in stations],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(constants.MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.departure_station.title, reply_markup=keyboard)
    return constants.DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """

    code, direction = await parse_data(update)
    stations: list[Station] = await get_app_data().controller.get_stations(direction, exclude_direction=True)
    buttons = [
        *[[InlineKeyboardButton(
            text=station.title,
            callback_data=await create_data(constants.SCHEDULE_VIEW, code, direction, station.code)
        )] for station in stations],
        [
            InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                                 callback_data=str(constants.MAIN_MENU)),
            InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                                 callback_data=str(constants.DEPARTURE_STATION))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.arrived_station.title, reply_markup=keyboard)
    return constants.ARRIVED_STATION


async def schedule_view(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    departure_code, direction, arrived_code = await parse_data(update)
    buttons = [
        [InlineKeyboardButton(text=MenuSections.arrived_station.back_to_title,
                              callback_data=await create_data(constants.ARRIVED_STATION,
                                                              departure_code, direction)),
         InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                              callback_data=str(constants.DEPARTURE_STATION))],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                              callback_data=str(constants.MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Расписание на ближайшее время', reply_markup=keyboard)
    return constants.SCHEDULE_VIEW
