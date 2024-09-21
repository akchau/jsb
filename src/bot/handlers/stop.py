from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("ОК, пока!")
    return ConversationHandler.END
