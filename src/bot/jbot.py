from logger import logger
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, filters, CallbackQueryHandler
)

from src.settings import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    departure_stations = [("Железнодорожная", "s343")]
    departure_buttons = [InlineKeyboardButton(station_name, callback_data=station_code)
                         for station_name, station_code in departure_stations]
    reply_markup = InlineKeyboardMarkup([departure_buttons])
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Станция отправления?",
        reply_markup=reply_markup
    )


async def handle_departure_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_station = query.data
    context.user_data['departure_station'] = selected_station

    arrival_stations = [("Москва", "m123"), ("Санкт-Петербург", "m456")]
    arrival_buttons = [InlineKeyboardButton(station_name, callback_data=station_code)
                       for station_name, station_code in arrival_stations]
    reply_markup = InlineKeyboardMarkup([arrival_buttons])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Станция прибытия?",
        reply_markup=reply_markup
    )


async def handle_arrival_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected_arrival_station = query.data
    context.user_data['arrival_station'] = selected_arrival_station

    departure_station = context.user_data.get('departure_station')
    arrival_station = context.user_data.get('arrival_station')

    buttons = ReplyKeyboardMarkup(
        [
            ["/В обратную сторону"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Загружаю расписание {departure_station}-{arrival_station}. Секундочку..."
    )
    schedule_pages = []
    for schedule_message in schedule_pages:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=schedule_message,
            reply_markup=buttons,
            parse_mode="html"
        )


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
    logger.info("Запуск бота.")
    # Инициализация приложения.
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    # Обработчик команды /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Обработчики для выбора станции отправления и станции прибытия
    departure_station_handler = CallbackQueryHandler(handle_departure_station, pattern=r'^s\d+$')
    arrival_station_handler = CallbackQueryHandler(handle_arrival_station, pattern=r'^m\d+$')

    application.add_handler(departure_station_handler)
    application.add_handler(arrival_station_handler)

    # Обработчик неизвестных команд
    echo_command_handler = MessageHandler(filters.COMMAND, not_known_command)
    application.add_handler(echo_command_handler)

    # Обработчик неизвестных сообщений
    echo_handler = MessageHandler(filters.TEXT, not_known_message)
    application.add_handler(echo_handler)

    logger.info("Бот запущен.")
    application.run_polling()
