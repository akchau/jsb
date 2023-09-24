
from bot.user_logger import log_user_decorator
from logger import logger
from bot.send_schedule import load_and_sent_schedule
from telegram import Update
from telegram.ext import (ApplicationBuilder, ContextTypes,
                          CommandHandler, MessageHandler, filters
)


import settings


@log_user_decorator
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Загружаю расписание. Секундочку..."
    )
    await load_and_sent_schedule(update, context)

@log_user_decorator
async def not_known_message(update: Update, context: ContextTypes.DEFAULT_TYPE):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Бот не значет что ответить("
    )

@log_user_decorator
async def not_known_command(update: Update, context: ContextTypes.DEFAULT_TYPE):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Бот не значет такую команду("
    )


def start_bot():
    logger.info("Запуск бота.")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    start_handler = CommandHandler('get', start)
    application.add_handler(start_handler)

    echo_command_handler = MessageHandler(filters.COMMAND, not_known_command)
    application.add_handler(echo_command_handler)

    echo_handler = MessageHandler(filters.TEXT, not_known_message)
    application.add_handler(echo_handler)

    logger.info("Бот запущен.")
    application.run_polling()
