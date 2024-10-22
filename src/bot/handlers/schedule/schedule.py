"""
Модуль обработчиков расписания
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *
from src.bot.handlers.data_handler import parse_data, create_data
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
    #---------------------------------------Получение контекста--------------------------------------------------------#
    data: tuple[str, str] | None = await parse_data(update)
    arrived_station_already_choice = True if data else None
    # ---------------------------------------------Контроллер----------------------------------------------------------#
    departure_stations = await get_app_data().controller.get_app(AppsEnum.ADMIN).departure_station_view(data)
    # -----------------------------------------------Клавиатура--------------------------------------------------------#
    if arrived_station_already_choice:
        arrived_station_code, _ = data
        context_data = [
            (
                departure_station_item.title,
                await create_data(
                    SCHEDULE_VIEW,
                    departure_station_item.code, departure_station_item.direction, arrived_station_code
                )
            ) for departure_station_item in departure_stations
        ]
    else:
        context_data = [
            (
                departure_station_item.title,
                await create_data(
                    ARRIVED_STATION,
                    departure_station_item.code, departure_station_item.direction
                )
            ) for departure_station_item in departure_stations
        ]
    buttons = [
        *[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data
                )
            ]
            for text, callback_data in context_data],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    # -----------------------------------------------Ответ бота--------------------------------------------------------#
    await clean_all_messages_upper(update, context)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.departure_station.title, reply_markup=keyboard)
    return DEPARTURE_STATION


async def arrived_station(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    # ---------------------------------------Получение контекста-------------------------------------------------------#
    data = await parse_data(update)
    departure_station_code, departure_station_direction = data
    # ---------------------------------------------Контроллер----------------------------------------------------------#
    available_arrived_station_list = await get_app_data().controller.get_app(AppsEnum.ADMIN).arrived_station_view(data)
    # -----------------------------------------------Клавиатура--------------------------------------------------------#
    buttons = [
        *[[InlineKeyboardButton(
            text=arrived_station_item.title,
            callback_data=await create_data(SCHEDULE_VIEW,
                                            departure_station_code,
                                            departure_station_direction,
                                            arrived_station_item.code))]
            for arrived_station_item in available_arrived_station_list],
        [
            InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                                 callback_data=str(MAIN_MENU)),
            InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                                 callback_data=str(DEPARTURE_STATION))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    # -----------------------------------------------Ответ бота--------------------------------------------------------#
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.arrived_station.title, reply_markup=keyboard)
    return ARRIVED_STATION


async def schedule_view(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик меню станции отправления.
    :param update:
    :param _:
    :return:
    """
    # ---------------------------------------Получение контекста-------------------------------------------------------#
    data = await parse_data(update)
    departure_code, direction, arrived_code = data
    # ---------------------------------------------Контроллер----------------------------------------------------------#
    schedule, departure_station_db, arrived_station_db = await get_app_data().schedule_controller.get_schedule(
        departure_code,
        arrived_code,
        direction
    )
    # -----------------------------------------------Клавиатура--------------------------------------------------------#
    buttons = [
        [InlineKeyboardButton(text=MenuSections.arrived_station.back_to_title,
                              callback_data=await create_data(str(ARRIVED_STATION),
                                                              departure_code, direction)),
         InlineKeyboardButton(text=MenuSections.departure_station.back_to_title,
                              callback_data=await create_data(str(DEPARTURE_STATION),
                                                              arrived_code, direction))],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title,
                              callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    # -----------------------------------------------Ответ бота--------------------------------------------------------#
    if update.callback_query:
        await update.callback_query.message.delete()
    await update.callback_query.answer()
    for time in schedule:
        await update.effective_message.reply_text(time)
    await update.effective_message.reply_text(f"Расписание {departure_station_db.title} - "
                                              f"{arrived_station_db.title}", reply_markup=keyboard)
    return SCHEDULE_VIEW
