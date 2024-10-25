"""
Модуль обработчиков расписания
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.utils import clean_all_messages_upper

from src.init_app import get_app_data


async def departure_station(update: Update,
                            context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param context:
    :return:
    """
    data: dict = await get_app_data().controller.apps.schedule.departure_station_view(update)
    buttons = [
        *[
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=callback_data
                )
            ]
            for title, callback_data in data["available_departure_stations_buttons"]],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await clean_all_messages_upper(update, context)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(data["message"], reply_markup=keyboard)
    return DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    data: dict = await get_app_data().controller.apps.schedule.arrived_station_view(update)
    buttons = [
        *[
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=callback_data
                )
            ]
            for title, callback_data in data["available_arrived_stations_buttons"]
        ],
        [
            InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                                 callback_data=str(MAIN_MENU)),
            InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                                 callback_data=str(DEPARTURE_STATION))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(data["message"], reply_markup=keyboard)
    return ARRIVED_STATION


async def schedule(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    data: dict = await get_app_data().controller.apps.schedule.schedule_view(update)
    change_arrived_station_button = data["change_arrived_station_button"]
    buttons = [
        *[
            [
                InlineKeyboardButton(*data["change_arrived_station_button"]),
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"{str(EDIT_STATION)}/{}"
                )
            ]
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                              callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.callback_query:
        await update.callback_query.message.delete()
    await update.callback_query.answer()
    for time in data["schedule"]:
        await update.effective_message.reply_text(time)
    await update.effective_message.reply_text(data["message"], reply_markup=keyboard)
    return SCHEDULE_VIEW
