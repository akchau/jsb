"""
Меню при регистрации станции.
"""
import logging

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *

from src.init_app import get_app_data


logger = logging.getLogger(__name__)


async def registered_stations_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    data: dict = await get_app_data().controller.apps.admin.registered_stations_with_direction_view(update)
    direction = data["direction"]
    buttons = [
        *[
             [
                 InlineKeyboardButton(text=title,
                                      callback_data=f"{str(EDIT_STATION)}/{callback_data}")
                 for title, callback_data in data["registered_stations_buttons"]
             ]
        ],
        [
            InlineKeyboardButton(text=MenuSections.my_stations.back_to_title,
                                 callback_data=str(REGISTERED_STATIONS)),
            InlineKeyboardButton(text=MenuSections.register_station_with_direction_from_moscow.back_to_title,
                                 callback_data=f"{str(REGISTER_STATION_WITH_DIRECTION)}/{direction}")

        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    text_direction = data["text_direction"]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        text=f"{MenuSections.my_stations.title}\nНаправление: {text_direction}",
        reply_markup=keyboard)
    return REGISTERED_STATIONS_WITH_DIRECTION
