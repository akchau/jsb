"""
Обработчик главного меню.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants


async def main_menu(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Главное меню - точка входа.
    """
    buttons = [
        [InlineKeyboardButton(text="Расписание", callback_data=str(constants.SCHEDULE)),
         InlineKeyboardButton(text="Админка", callback_data=str(constants.ADMIN))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        await update.message.reply_text('Главное меню.', reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text('Главное меню.', reply_markup=keyboard)
    return constants.MAIN_MENU
