"""
Обработчик главного меню.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot.handlers.handler_types import *


async def main_menu(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Главное меню - точка входа.
    """
    buttons = [
        [InlineKeyboardButton(text=MenuSections.schedule.title, callback_data=str(DEPARTURE_STATION)),
         InlineKeyboardButton(text=MenuSections.admin_zone.title, callback_data=str(ADMIN))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        await update.message.reply_text(MenuSections.main_menu.title, reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text(MenuSections.main_menu.title, reply_markup=keyboard)
    return MAIN_MENU


async def admin(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Меню админа.
    """
    buttons = [
        [
            InlineKeyboardButton(text=MenuSections.register_station.title, callback_data=str(REGISTER_STATION)),
            InlineKeyboardButton(text=MenuSections.my_stations.title, callback_data=str(REGISTERED_STATIONS)),
        ],
        [InlineKeyboardButton(text=MenuSections.main_menu.back_to_title, callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(MenuSections.admin_zone.title, reply_markup=keyboard)
    return ADMIN