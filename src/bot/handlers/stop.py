"""
Обработчик остановки бота
"""
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def stop(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Остановка бота
    :param update:
    :param _:
    :return:
    """
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("ОК, пока!")
    return ConversationHandler.END
