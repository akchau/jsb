import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from src.controller.controller_types import StationsDirection
from src.init_app import get_app_data
from src.settings import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


SELECTING_ACTION, ADMIN_MENU, SCHEDULE, ADD_STATION, MY_STATIONS, FROM_MOSCOW, TO_MOSCOW, SELECT_DIRECTION, ADD_FROM_MOSCOW, ADD_TO_MOSCOW = range(10)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Админка", callback_data=str(ADMIN_MENU)),
            InlineKeyboardButton(text="расписание", callback_data=str(SCHEDULE)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    if update.message:
        await update.message.reply_text('Пожалуйста, выберите вариант:', reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text('Пожалуйста, выберите вариант:', reply_markup=keyboard)

    return SELECTING_ACTION

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Добавить станцию", callback_data=str(ADD_STATION)),
            InlineKeyboardButton(text="Мои станции", callback_data=str(MY_STATIONS)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(SELECTING_ACTION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите действие:", reply_markup=keyboard)
    return ADMIN_MENU

async def add_station(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы", callback_data=str(ADD_FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(ADD_TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление для добавления станции:", reply_markup=keyboard)
    return SELECT_DIRECTION

async def add_station_from_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(ADD_STATION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали добавить станцию из Москвы.", reply_markup=keyboard)
    # Здесь добавьте вашу логику для добавления станций из Москвы
    return ADD_FROM_MOSCOW

async def add_station_to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(ADD_STATION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали добавить станцию в Москву.", reply_markup=keyboard)
    # Здесь добавьте вашу логику для добавления станций в Москву
    return ADD_TO_MOSCOW

async def my_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы", callback_data=str(FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление:", reply_markup=keyboard)
    return MY_STATIONS

async def from_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(MY_STATIONS))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.FROM_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции из Москвы:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return FROM_MOSCOW

async def to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(MY_STATIONS))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.TO_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции в Москву:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return TO_MOSCOW

async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(SELECTING_ACTION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали расписание.", reply_markup=keyboard)
    return SCHEDULE

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("ОК, пока!")
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(settings.BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN_MENU) + "$"),
                CallbackQueryHandler(schedule, pattern="^" + str(SCHEDULE) + "$")
            ],
            ADMIN_MENU: [
                CallbackQueryHandler(add_station, pattern="^" + str(ADD_STATION) + "$"),
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$"),
                CallbackQueryHandler(start, pattern="^" + str(SELECTING_ACTION) + "$")
            ],
            ADD_STATION: [
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN_MENU) + "$")
            ],
            SELECT_DIRECTION: [
                CallbackQueryHandler(add_station_from_moscow, pattern="^" + str(ADD_FROM_MOSCOW) + "$"),
                CallbackQueryHandler(add_station_to_moscow, pattern="^" + str(ADD_TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN_MENU) + "$")
            ],
            MY_STATIONS: [
                CallbackQueryHandler(from_moscow, pattern="^" + str(FROM_MOSCOW) + "$"),
                CallbackQueryHandler(to_moscow, pattern="^" + str(TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN_MENU) + "$")
            ],
            FROM_MOSCOW: [
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$")
            ],
            TO_MOSCOW: [
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$")
            ],
            SCHEDULE: [
                CallbackQueryHandler(start, pattern="^" + str(SELECTING_ACTION) + "$")
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()