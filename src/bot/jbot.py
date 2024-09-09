from logger import logger
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, filters, CallbackQueryHandler
)

from src.settings import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Из Москвы", callback_data='schedule_from_moscow')],
        [InlineKeyboardButton("В Москву", callback_data='schedule_to_moscow')]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="В какую сторону?",
        reply_markup=reply_markup
    )


async def get_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'schedule_from_moscow':
        schedule_direction = "Из Москвы"
    elif query.data == 'schedule_to_moscow':
        schedule_direction = "В Москву"
    else:
        raise Exception("Неизвестное расписание")

    buttons = ReplyKeyboardMarkup(
        [
            ["/В обратную сторону"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Загружаю расписание {schedule_direction}. Секундочку..."
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

    get_schedule_handler = CallbackQueryHandler(get_schedule, pattern='schedule_.*')
    application.add_handler(get_schedule_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_command_handler = MessageHandler(filters.COMMAND, not_known_command)
    application.add_handler(echo_command_handler)

    echo_handler = MessageHandler(filters.TEXT, not_known_message)
    application.add_handler(echo_handler)

    logger.info("Бот запущен.")
    application.run_polling()
