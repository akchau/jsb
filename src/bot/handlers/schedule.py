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
    available_departure_stations_buttons = data["available_departure_stations_buttons"]
    message = data["message"]
    redirect_to_schedule = data["redirect_to_schedule"]
    back_to_main_menu_button_title = data["back_to_main_menu_button_title"]
    path = SCHEDULE if redirect_to_schedule else ARRIVED_STATION
    buttons = [
        # Кнопки "СТАНЦИЯ ОТПРАВЛЕНИЯ"
        *[[InlineKeyboardButton(text=title, callback_data=f"{str(path)}{callback_data}")]
          for title, callback_data in available_departure_stations_buttons],

        # Кнопка "ГЛАВНОЕ МЕНЮ"
        [InlineKeyboardButton(text=back_to_main_menu_button_title, callback_data=str(MAIN_MENU))]

    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await clean_all_messages_upper(update, context)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message, reply_markup=keyboard)
    return DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    data: dict = await get_app_data().controller.apps.schedule.arrived_station_view(update)
    available_arrived_stations_buttons: list[tuple[str, str]] = data["available_arrived_stations_buttons"]
    message: str = data["message"]
    back_to_menu_title: str = data["back_to_menu_title"]
    back_to_departure_station_button: tuple[str, str] = data["back_to_departure_station_button"]
    buttons = [
        *[
            # Кнопки "СТАНЦИЯ ПРИБЫТИЯ"
            [InlineKeyboardButton(text=title, callback_data=f"{SCHEDULE}{callback_data}")]
            for title, callback_data in available_arrived_stations_buttons
        ],
        # Кнопка "ВЫБОР СТАНЦИИ ОТПРАВЛЕНИЯ"
        [InlineKeyboardButton(text=back_to_departure_station_button[0],
                              callback_data=f"{str(SCHEDULE)}{back_to_departure_station_button[1]}")],
        # Кнопка "ГЛАВНОЕ МЕНЮ"
        [InlineKeyboardButton(text=back_to_menu_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(message, reply_markup=keyboard)
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
    change_departure_station_button = data["change_departure_station_button"]
    paginated_schedule = data["schedule"]
    back_to_menu_title = data["back_to_menu_title"]
    message = data["message"]
    buttons = [
        [
            # Кнопка "СМЕНИТЬ СТАНЦИЮ ОТПРАВЛЕНИЯ"
            InlineKeyboardButton(text=change_departure_station_button[0],
                                 callback_data=f"{str(DEPARTURE_STATION)}{change_departure_station_button[1]}"),
            # Кнопка "СМЕНИТЬ СТАНЦИЮ ПРИБЫТИЯ"
            InlineKeyboardButton(text=change_arrived_station_button[0],
                                 callback_data=f"{str(ARRIVED_STATION)}{change_arrived_station_button[1]}")
        ],
        # Кнопка "ГЛАВНОЕ МЕНЮ"
        [InlineKeyboardButton(text=back_to_menu_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.callback_query:
        await update.callback_query.message.delete()
    await update.callback_query.answer()
    for time in paginated_schedule:
        await update.effective_message.reply_text(time)
    await update.effective_message.reply_text(message, reply_markup=keyboard)
    return SCHEDULE
