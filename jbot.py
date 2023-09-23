import logging

from telegram import Update
from telegram.ext import (ApplicationBuilder, ContextTypes,
                          CommandHandler, MessageHandler, filters)
from send_schdule import ScheduleSender
import settings

DEBUG_FILE = True

logger = logging.getLogger(__name__)

if settings.DEBUG and DEBUG_FILE:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
logger.addHandler(handler)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=ScheduleSender({}).get_shedule()
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    application.run_polling()
