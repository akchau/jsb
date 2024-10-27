"""
Обработчик главного меню.
"""
import logging

from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *

logger = logging.getLogger(__name__)


async def main_menu(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Главное меню - точка входа.
    """
    user = update.message.from_user if update.message else update.callback_query.from_user
    logger.debug(
        f"ID={user.id}, {user.username}, {user.first_name}, {user.last_name} запустил бота.")
    buttons = [
        [InlineKeyboardButton(text="Расписание", callback_data=str(DEPARTURE_STATION)),
         InlineKeyboardButton(text="Админка",
                              callback_data=str(REGISTERED_STATIONS_WITH_DIRECTION))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        await update.message.reply_text("Главное меню", reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text("Главное меню", reply_markup=keyboard)
    return MAIN_MENU
