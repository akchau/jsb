"""
Модуль с обработчиками регистрации станций
"""
import logging

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *

from src.init_app import get_app_data


logger = logging.getLogger(__name__)


async def register_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    data = await get_app_data().controller.apps.admin.register_station_view(update)
    buttons = [
        [
            *[InlineKeyboardButton(
                text=text_direction,
                callback_data=f"{str(REGISTER_STATION_WITH_DIRECTION)}/{direction}"
            ) for text_direction, direction in data["directions"]],

        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=MenuSections.register_station.title, reply_markup=keyboard)
    return REGISTER_STATION


async def register_station_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик регистрации станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    data = await get_app_data().controller.apps.admin.register_station_with_direction_view(update)
    direction = data["direction"]
    buttons = [
        *[
            [
                InlineKeyboardButton(text=title,
                                     callback_data=f"{str(REGISTERED_STATIONS_WITH_DIRECTION)}/{callback_data}")
                for title, callback_data in data["callback_data"]
            ]
        ],

        [
            InlineKeyboardButton(text=MenuSections.register_station.back_to_title, callback_data=str(REGISTER_STATION)),
            InlineKeyboardButton(text=MenuSections.registered_station_with_direction_to_moscow.back_to_title,
                                 callback_data=f"{str(REGISTERED_STATIONS_WITH_DIRECTION)}/{direction}")
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    text_direction = data["available_stations"]
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=f"Доступные для регистрации станции\nНаправление: {text_direction}",
        reply_markup=keyboard
    )
    return REGISTER_STATION_WITH_DIRECTION
