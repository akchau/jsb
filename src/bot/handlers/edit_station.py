"""
Обработчик редактирования зарегистрированных станций.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.bot.bot_types import MenuSections
from src.bot.handlers.data_handler import parse_data, create_data

from src.controller.controller_types import StationActionEnum


async def edit_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    direction, code, title = await parse_data(update)
    buttons = [
        [
            InlineKeyboardButton(
                text=MenuSections.delete.title,
                callback_data=await create_data(
                    constants.REGISTERED_STATIONS_WITH_DIRECTION,
                    direction, StationActionEnum.DELETE, code
                )
            )
        ],
        [InlineKeyboardButton(
            text=MenuSections.move.title,
            callback_data=await create_data(constants.REGISTERED_STATIONS_WITH_DIRECTION,
                                            direction, StationActionEnum.MOVE, code))],
        [InlineKeyboardButton(
            text=MenuSections.registered_station_with_direction_to_moscow.back_to_title,
            callback_data=await create_data(constants.REGISTERED_STATIONS_WITH_DIRECTION,
                                            direction))],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(constants.MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Выберите действие со станцией {title}:", reply_markup=keyboard)
    return constants.EDIT_STATION
