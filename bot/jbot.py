
from api_client.pollers.reset_poller import start_reset_poller
from bot.user_logger import log_user_decorator
from shedule_manager.schedule_saver import get_shedule_key
from logger import logger
from bot.send_schedule import load_and_sent_schedule
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, filters
)

import settings


@log_user_decorator
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = ReplyKeyboardMarkup(
        [
            ["/to_jheldor"],
            ["/to_moscow"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="В какую сторону?",
        reply_markup=buttons
    )


@log_user_decorator
async def get_to_jheldor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = ReplyKeyboardMarkup(
        [
            ["/to_moscow"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Загружаю расписание. Секундочку..."
    )
    await load_and_sent_schedule(
        update,
        context,
        buttons,
        departure_station_code=settings.NIJEGORODSKAYA["code"],
        arrived_station_code=settings.JELEZNODOROJNAYA["code"]
    )


@log_user_decorator
async def get_to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = ReplyKeyboardMarkup(
        [
            ["/to_jheldor"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Загружаю расписание. Секундочку..."
    )
    key = get_shedule_key(settings.JELEZNODOROJNAYA["code"], settings.NIJEGORODSKAYA["code"])
    await load_and_sent_schedule(
        update,
        context,
        buttons,
        departure_station_code=settings.JELEZNODOROJNAYA["code"],
        arrived_station_code=settings.NIJEGORODSKAYA["code"]
    )


@log_user_decorator
async def not_known_message(update: Update, context: ContextTypes.DEFAULT_TYPE):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    buttons = ReplyKeyboardMarkup(
        [
            ["/start"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Бот не значет что ответить(",
        reply_markup=buttons
    )


@log_user_decorator
async def not_known_command(update: Update, context: ContextTypes.DEFAULT_TYPE):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
    buttons = ReplyKeyboardMarkup(
        [
            ["/start"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Бот не значет такую команду(",
        reply_markup=buttons
    )


def start_bot():
    start_reset_poller()
    logger.info("Запуск бота.")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    to_jheldor_handler = CommandHandler('to_jheldor', get_to_jheldor)
    application.add_handler(to_jheldor_handler)

    to_moscow_handler = CommandHandler('to_moscow', get_to_moscow)
    application.add_handler(to_moscow_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_command_handler = MessageHandler(filters.COMMAND, not_known_command)
    application.add_handler(echo_command_handler)

    echo_handler = MessageHandler(filters.TEXT, not_known_message)
    application.add_handler(echo_handler)

    logger.info("Бот запущен.")
    application.run_polling()
