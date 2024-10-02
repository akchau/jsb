"""
Меню при регистрации станции.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants
from src.bot.bot_types import StationActions
from src.controller.controller_types import StationsDirection
from src.init_app import get_app_data


async def registered_stations(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Обработчик меню регистрации станции.
    :param update:
    :param _:
    :return:
    """
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы 🏡🚄🏢", callback_data=f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{StationsDirection.FROM_MOSCOW}"),
            InlineKeyboardButton(text="В Москву 🏢🚄🏡", callback_data=f"{constants.REGISTERED_STATIONS_WITH_DIRECTION}/{StationsDirection.TO_MOSCOW}"),
        ],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Мои станции 🛤", reply_markup=keyboard)
    return constants.REGISTERED_STATIONS


async def registered_stations_with_direction(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станций от Москвы.
    :param update:
    :param _:
    :return:
    """
    query = update.callback_query
    data = query.data
    direction = data.split("/")[1]
    if len(data.split("/")) == 4:
        action = data.split("/")[2]
        code = data.split("/")[3]
        if action == StationActions.REGISTER:
            await get_app_data().controller.register_new_station(direction=direction, code=code)
        elif action == StationActions.MOVE:
            await get_app_data().controller.move_station(direction=direction, code=code)
        elif action == StationActions.DELETE:
            await get_app_data().controller.delete_station(direction=direction, code=code)
    stations = await get_app_data().controller.get_registered_stations(direction=direction)

    buttons = [
        *[[InlineKeyboardButton(station.title, callback_data=f"{constants.EDIT_STATION}/{direction}/{station.code}")]
          for station in stations],
        [InlineKeyboardButton(text="Назад к выбору направления 🛤⬅️", callback_data=str(constants.REGISTERED_STATIONS))],
        [InlineKeyboardButton(text="Назад в меню Администратора 🔴⬅️", callback_data=str(constants.ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()

    if direction == StationsDirection.FROM_MOSCOW:
        text_direction = "Из Москвы 🏡🚄🏢"
    elif direction == StationsDirection.TO_MOSCOW:
        text_direction = "В Москву 🏢🚄🏡"

    await update.callback_query.edit_message_text(text=f"Станции зарегистрированные {text_direction}", reply_markup=keyboard)

    return constants.REGISTERED_STATIONS_WITH_DIRECTION