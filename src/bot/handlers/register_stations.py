"""
Модуль с обработчиками регистрации станций
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.controller.controller_types import StationsDirection, DirectionType, StationActionEnum
from src.init_app import get_app_data


async def register_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="Из Москвы 🏡🚄🏢",
                callback_data=f"{constants.REGISTER_STATION_WITH_DIRECTION}/{StationsDirection.FROM_MOSCOW}"
            ),
            InlineKeyboardButton(
                text="В Москву 🏢🚄🏡",
                callback_data=f"{constants.REGISTER_STATION_WITH_DIRECTION}/{StationsDirection.TO_MOSCOW}"
            )
        ],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Новая станция 🆕",
                                                  reply_markup=keyboard)
    return constants.REGISTER_STATION


async def register_station_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик регистрации станций от Москвы.
    :param update:
    :param _:
    :return:
    """

    query = update.callback_query
    data = query.data
    direction = data.split("/")[1]

    stations = await get_app_data().controller.get_stations(direction, for_registration=True)

    buttons = [
        *[[InlineKeyboardButton(text=station.title,
                                callback_data=(f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{direction}/"
                                               f"{StationActionEnum.REGISTER}/{station.code}"))]
          for station in stations],
        [InlineKeyboardButton(text="Назад к выбору направления 🆕⬅️", callback_data=str(constants.REGISTER_STATION))],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text_direction = DirectionType(direction=direction).get_text_direction()

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Доступные станции {text_direction}", reply_markup=keyboard)
    return constants.REGISTER_STATION_WITH_DIRECTION
