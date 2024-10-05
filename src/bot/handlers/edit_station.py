"""
Обработчик редактирования зарегистрированных станций.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants

from src.controller.controller_types import StationActionEnum


async def edit_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """

    query = update.callback_query
    data = query.data
    direction = data.split("/")[1]
    code = data.split("/")[2]

    buttons = [
        [InlineKeyboardButton(
            text="Удалить ❌",
            callback_data=(f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{direction}"
                           f"/{StationActionEnum.DELETE}/{code}"))],
        [InlineKeyboardButton(
            text="Переместить 🔁",
            callback_data=(f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{direction}/{StationActionEnum.MOVE}"
                           f"/{code}"))],
        [InlineKeyboardButton(
            text="Назад к списку зарегистрированных станций 🛤⬅️",
            callback_data=f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{direction}")]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Выберите действие со станцией {code}:", reply_markup=keyboard)
    return constants.EDIT_STATION
