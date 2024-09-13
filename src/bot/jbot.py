from logger import logger
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          MessageHandler, filters, CallbackQueryHandler, ConversationHandler
                          )

from src.init_app import get_app_data
from src.settings import settings


STATION_SELECTION, DIRECTION_SELECTION = range(2)


async def register_new_station(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """В начале разговора узнать какую станцию из предложенного списка зарегистрировать."""
    stations = await get_app_data().controller.get_available_for_registration_stations()

    departure_buttons = [[KeyboardButton(station_name)] for station_name, station_code in stations]

    await update.message.reply_text(
        "Какую станцию необходимо зарегистрировать?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=departure_buttons,
            one_time_keyboard=True,
            input_field_placeholder="Станция?",
            resize_keyboard=True
        ),
    )

    return STATION_SELECTION


async def select_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data['station'] = query.data

    directions = ["North", "South", "East", "West"]
    direction_buttons = [[InlineKeyboardButton(direction, callback_data=direction)] for direction in directions]
    reply_markup = InlineKeyboardMarkup(direction_buttons)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выберите направление",
        reply_markup=reply_markup
    )
    return DIRECTION_SELECTION


async def select_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['direction'] = query.data
    get_app_data().controller.register_new_station(context.user_data['station'])
    print("Направление", context.user_data['direction'])
    return ConversationHandler.END


async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    station_code = query.data
    await query.answer()
    get_app_data().controller.register_new_station(station_code)
    await admin_zone(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Админ зона"), KeyboardButton("Расписание")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Выберите опцию:', reply_markup=reply_markup)


async def admin_zone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        ["Зарегистрировать", "Мои станции"],
        ["Назад"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('Админ зона:', reply_markup=reply_markup)


async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start(update, context)


async def my_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    stations = get_app_data().controller.get_registered_stations()
    if not stations:
        if update.callback_query:
            await update.callback_query.edit_message_text('У вас нет зарегистрированных станций.')
        else:
            await update.message.reply_text('У вас нет зарегистрированных станций.')
    else:
        keyboard = [[InlineKeyboardButton(station[0], callback_data='noop')] for station in stations]
        keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.callback_query:
            await update.callback_query.edit_message_text('Ваши станции:', reply_markup=reply_markup)
        else:
            await update.message.reply_text('Ваши станции:', reply_markup=reply_markup)


async def not_known_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = ReplyKeyboardMarkup(
        [
            ["/start"],
        ],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Бот не знает что ответить(",
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
        text="Бот не знает такую команду(",
        reply_markup=buttons
    )


def start_bot():
    logger.info("Запуск бота.")
    application = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text(["Админ зона"]), admin_zone))
    application.add_handler(MessageHandler(filters.Text(["Назад"]), back_to_main))
    application.add_handler(MessageHandler(filters.Text(["Зарегистрировать"]), register))
    application.add_handler(MessageHandler(filters.Text(["Мои станции"]), my_stations))
    application.add_handler(CallbackQueryHandler(register_handler))
    logger.info("Бот запущен.")
    application.run_polling()


if __name__ == '__main__':
    start_bot()
