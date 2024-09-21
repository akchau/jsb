from telegram import InlineKeyboardButton, Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.bot import constants


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Вы выбрали расписание.', reply_markup=keyboard)
    return constants.SCHEDULE


async def departure_station(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(constants.SCHEDULE))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Вы выбрали расписание.', reply_markup=keyboard)
    return constants.DEPARTURE_STATION
