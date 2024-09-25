"""
Меню при регистрации станции.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.controller.controller_types import StationsDirection
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
            InlineKeyboardButton(text="Из Москвы", callback_data=str(constants.REGISTERED_STATIONS_FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(constants.REGISTERED_STATIONS_TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление:", reply_markup=keyboard)
    return constants.REGISTERED_STATIONS


async def registered_stations_from_moscow(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.REGISTERED_STATIONS))],
        [InlineKeyboardButton(text="Админка", callback_data=str(constants.ADMIN))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.FROM_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции из Москвы:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return constants.REGISTERED_STATIONS_FROM_MOSCOW


async def registered_stations_to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.REGISTERED_STATIONS))],
        [InlineKeyboardButton(text="Админка", callback_data=str(constants.ADMIN))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.TO_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции в Москву:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return constants.REGISTERED_STATIONS_TO_MOSCOW
