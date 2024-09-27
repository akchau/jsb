"""
Модуль с обработчиками регистрации станций
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.controller.controller_types import StationsDirection
from src.init_app import get_app_data


async def register_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы", callback_data=str(constants.REGISTER_STATION_FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(constants.REGISTER_STATION_TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление для регистрации станции:",
                                                  reply_markup=keyboard)
    return constants.REGISTER_STATION


async def register_station_from_moscow(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик регистрации станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    stations = await get_app_data().controller.get_available_for_registration_stations_in_direction(
        StationsDirection.FROM_MOSCOW)

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.REGISTER_STATION))],
        [InlineKeyboardButton(text="Админка", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Доступные станции {stations}", reply_markup=keyboard)
    return constants.REGISTER_STATION_FROM_MOSCOW


async def register_station_to_moscow(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик регистраций станций.
    :param update:
    :param _:
    :return:
    """
    stations = await get_app_data().controller.get_available_for_registration_stations_in_direction(
        StationsDirection.TO_MOSCOW)

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.REGISTER_STATION))],
        [InlineKeyboardButton(text="Админка", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Доступные станции {stations}", reply_markup=keyboard)
    return constants.REGISTER_STATION_TO_MOSCOW
