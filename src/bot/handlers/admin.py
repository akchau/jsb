"""
Обработчики админки.
"""
from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants


async def admin(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Меню админа.
    """
    buttons = [
        [
            InlineKeyboardButton(text="Добавить станцию", callback_data=str(constants.REGISTER_STATION)),
            InlineKeyboardButton(text="Мои станции", callback_data=str(constants.REGISTERED_STATIONS)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Админка: выберите действие:', reply_markup=keyboard)
    return constants.ADMIN
