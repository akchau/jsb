"""
Меню при регистрации станции.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.controller.controller_types import StationsDirection, DirectionType, StationActionEnum
from src.init_app import get_app_data


async def registered_stations(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню регистрации станции.
    :param update:
    :param _:
    :return:
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="Из Москвы 🏡🚄🏢",
                callback_data=f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{StationsDirection.FROM_MOSCOW}"
            ),
            InlineKeyboardButton(
                text="В Москву 🏢🚄🏡",
                callback_data=f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{StationsDirection.TO_MOSCOW}"
            ),
        ],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Мои станции 🛤", reply_markup=keyboard)
    return constants.REGISTERED_STATIONS


async def registered_stations_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    query = update.callback_query
    data = query.data
    direction = data.split("/")[1]
    if len(data.split("/")) == 4:
        action: StationActionEnum = data.split("/")[2]
        code = data.split("/")[3]
        await get_app_data().controller.station_action(direction=direction, code=code, action=action)

    stations = await get_app_data().controller.get_stations(direction=direction)

    buttons = [
        *[[InlineKeyboardButton(station.title, callback_data=f"{constants.EDIT_STATION}/{direction}/{station.code}")]
          for station in stations],
        [InlineKeyboardButton(text="Назад к выбору направления 🛤⬅️", callback_data=str(constants.REGISTERED_STATIONS))],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()

    text_direction = DirectionType(direction=direction).get_text_direction()

    await update.callback_query.edit_message_text(
        text=f"Зарегистрированные станции:\nНаправление: {text_direction}",
        reply_markup=keyboard)

    return constants.REGISTERED_STATIONS_WITH_DIRECTION
