"""
Модуль с обработчиками регистрации станций
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.handlers.data_handler import parse_data, create_data

from src.init_app import get_app_data


async def register_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    directions = await get_app_data().controller.get_directions()
    buttons = [
        [
            *[InlineKeyboardButton(
                text=MenuSections.register_station_with_direction_from_moscow.title,
                callback_data=await create_data(REGISTER_STATION_WITH_DIRECTION,
                                                direction)
            ) for direction in directions.__members__],

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

    direction = await parse_data(update)
    stations, action, text_direction = await get_app_data().controller.get_stations(direction, for_registration=True)
    print(stations, action, text_direction)
    buttons = [
        *[[InlineKeyboardButton(text=station.title,
                                callback_data=(await create_data(REGISTERED_STATIONS_WITH_DIRECTION,
                                                                 direction, action,
                                                                 station.code)))]
          for station in stations],
        [
            InlineKeyboardButton(
                text=MenuSections.register_station.back_to_title,
                callback_data=str(REGISTER_STATION)),
            InlineKeyboardButton(
                text=MenuSections.registered_station_with_direction_to_moscow.back_to_title,
                callback_data=await create_data(
                    REGISTERED_STATIONS_WITH_DIRECTION,
                    direction)
            )
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))],
        [InlineKeyboardButton(text=MenuSections.admin_zone.back_to_title, callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    print(text_direction)
    await update.callback_query.edit_message_text(text=f"Доступные для регистрации станции\nНаправление: {text_direction}",
                                                  reply_markup=keyboard)
    return REGISTER_STATION_WITH_DIRECTION
