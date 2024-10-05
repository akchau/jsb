"""
Обработчик редактирования зарегистрированных станций.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.handlers.data_handler import parse_data, create_data

from src.init_app import get_app_data


async def edit_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    direction, code, title = await parse_data(update)
    delete_action, move_action = await get_app_data().controller.get_edit_menu_values()

    buttons = [
        [
            InlineKeyboardButton(
                text=MenuSections.delete.title,
                callback_data=await create_data(
                    REGISTERED_STATIONS_WITH_DIRECTION,
                    direction, delete_action, code
                )
            )
        ],
        [InlineKeyboardButton(
            text=MenuSections.move.title,
            callback_data=await create_data(REGISTERED_STATIONS_WITH_DIRECTION,
                                            direction, move_action, code))],
        [InlineKeyboardButton(
            text=MenuSections.registered_station_with_direction_to_moscow.back_to_title,
            callback_data=await create_data(REGISTERED_STATIONS_WITH_DIRECTION,
                                            direction))],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Выберите действие со станцией {title}:", reply_markup=keyboard)
    return EDIT_STATION
