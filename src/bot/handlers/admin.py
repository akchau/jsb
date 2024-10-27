"""
Модуль с обработчиками регистрации станций
"""
import logging

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.init_app import get_app_data


logger = logging.getLogger(__name__)


async def edit_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
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
    await update.callback_query.edit_message_text(text=f"Выберите действие со станцией {station.title}:", reply_markup=keyboard)
    return EDIT_STATION


async def register_station_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик регистрации станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    data = await get_app_data().controller.apps.admin.register_station_with_direction_view(update)
    direction = data["direction"]
    available_stations_buttons = data["available_stations_buttons"]
    message = data["message"]
    buttons = [
        *[
            [
                InlineKeyboardButton(text=title,
                                     callback_data=f"{str(REGISTERED_STATIONS_WITH_DIRECTION)}{callback_data}")
                for title, callback_data in available_stations_buttons
            ]
        ],

        [
            InlineKeyboardButton(text=MenuSections.registered_station_with_direction_to_moscow.back_to_title,
                                 callback_data=f"{str(REGISTERED_STATIONS_WITH_DIRECTION)}/{direction}")
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=message, reply_markup=keyboard)
    return REGISTER_STATION_WITH_DIRECTION


async def registered_stations_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    data: dict = await get_app_data().controller.apps.admin.registered_stations_with_direction_view(update)
    registered_stations_another_direction_button = data["registered_stations_another_direction_button"]
    register_stations_current_direction_button = data["register_stations_current_direction_button"]
    message = data["message"]
    registered_stations_buttons = data["registered_stations_buttons"]
    back_to_menu_title = data["back_to_menu_title"]
    buttons = [
        *[
             # Кнопки "РЕДАКТИРОВАТЬ"
             [
                 InlineKeyboardButton(text=title,
                                      callback_data=f"{str(EDIT_STATION)}/{callback_data}")
                 for title, callback_data in registered_stations_buttons
             ]
        ],
        [
            # Кнопка "СМЕНИТЬ НАПРВЛЕНИЕ"
            InlineKeyboardButton(
                text=registered_stations_another_direction_button[0],
                callback_data=f"{str(REGISTERED_STATIONS_WITH_DIRECTION)}"
                              f"/{registered_stations_another_direction_button[1]}"),
            # Кнопка "ЗАРЕГИСТРИРОВАТЬ"
            InlineKeyboardButton(
                text=register_stations_current_direction_button[0],
                callback_data=f"{str(REGISTER_STATION_WITH_DIRECTION)}"
                              f"/{register_stations_current_direction_button[1]}")

        ],
        # Кнопки "ГЛАВНОЕ МЕНЮ"
        [InlineKeyboardButton(text=back_to_menu_title, callback_data=str(MAIN_MENU))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message, reply_markup=keyboard)
    return REGISTERED_STATIONS_WITH_DIRECTION
