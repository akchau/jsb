"""
Модуль обработчиков расписания
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.init_app import get_app_data


async def departure_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    stations = await get_app_data().controller.get_registered_stations()
    buttons = [
        [InlineKeyboardButton(text="Главное меню", callback_data=str(constants.MAIN_MENU))],
        *[[InlineKeyboardButton(text=station.title, callback_data=f"{constants.ARRIVED_STATION}/"
                                                                  f"{station.code}/{station.direction}")]
          for station in stations]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Станция отправления', reply_markup=keyboard)
    return constants.DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """

    query = update.callback_query
    data = query.data
    departure_code = data.split("/")[1]
    direction = data.split("/")[2]
    stations = await get_app_data().controller.get_registered_stations(direction, exclude_direction=True)

    buttons = [
        *[[InlineKeyboardButton(
            text=station.title,
            callback_data=f"{constants.SCHEDULE_VIEW}/{departure_code}/{station.code}"
        )]
          for station in stations],
        [InlineKeyboardButton(text="Главное меню", callback_data=str(constants.MAIN_MENU))],
        [InlineKeyboardButton(text="Станция отправления", callback_data=str(constants.DEPARTURE_STATION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Станция прибытия', reply_markup=keyboard)
    return constants.ARRIVED_STATION


async def schedule_view(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """

    query = update.callback_query
    data = query.data
    departure_code = data.split("/")[1]
    arrived_code = data.split("/")[2]
    print(departure_code, arrived_code)
    buttons = [
        [InlineKeyboardButton(text="Станция прибытия", callback_data=str(constants.ARRIVED_STATION))],
        [InlineKeyboardButton(text="Станция отправления", callback_data=str(constants.DEPARTURE_STATION))],
        [InlineKeyboardButton(text="Главное меню", callback_data=str(constants.MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Расписание на ближайшее время', reply_markup=keyboard)
    return constants.SCHEDULE_VIEW
