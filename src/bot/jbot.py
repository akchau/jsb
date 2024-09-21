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


(MAIN_MENU, ADMIN, REGISTER_STATION, REGISTER_STATION_FROM_MOSCOW, REGISTER_STATION_TO_MOSCOW,
 REGISTERED_STATIONS, REGISTERED_STATIONS_FROM_MOSCOW, REGISTERED_STATIONS_TO_MOSCOW, SCHEDULE) = range(10)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Главное меню - точка входа.
    """
    buttons = [
        [InlineKeyboardButton(text="Расписание", callback_data=str(SCHEDULE)),
         InlineKeyboardButton(text="Админка", callback_data=str(ADMIN))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if update.message:
        await update.message.reply_text('Главное меню.', reply_markup=keyboard)
    else:
        await update.callback_query.edit_message_text('Главное меню.', reply_markup=keyboard)
    return MAIN_MENU


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Админка
    """
    buttons = [
        [
            InlineKeyboardButton(text="Добавить станцию", callback_data=str(REGISTER_STATION)),
            InlineKeyboardButton(text="Мои станции", callback_data=str(REGISTERED_STATIONS)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Админка: выберите действие:', reply_markup=keyboard)
    return ADMIN


async def register_station(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Регистрация станции.
    """
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы", callback_data=str(REGISTER_STATION_FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(REGISTER_STATION_TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление для регистрации станции:",
                                                  reply_markup=keyboard)
    return REGISTER_STATION


async def register_station_from_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    stations = await get_app_data().controller.get_available_for_registration_stations_in_direction(
        StationsDirection.FROM_MOSCOW)

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(REGISTER_STATION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Доступные станции {stations}", reply_markup=keyboard)
    return REGISTER_STATION_FROM_MOSCOW


async def register_station_to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    stations = await get_app_data().controller.get_available_for_registration_stations_in_direction(
        StationsDirection.TO_MOSCOW)

    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(REGISTER_STATION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=f"Доступные станции {stations}", reply_markup=keyboard)
    return REGISTER_STATION_TO_MOSCOW


async def registered_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [
            InlineKeyboardButton(text="Из Москвы", callback_data=str(REGISTERED_STATIONS_FROM_MOSCOW)),
            InlineKeyboardButton(text="В Москву", callback_data=str(REGISTERED_STATIONS_TO_MOSCOW)),
        ],
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Выберите направление:", reply_markup=keyboard)
    return REGISTERED_STATIONS


async def registered_stations_from_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(REGISTERED_STATIONS))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.FROM_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции из Москвы:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return REGISTERED_STATIONS_FROM_MOSCOW


async def registered_stations_to_moscow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(REGISTERED_STATIONS))]
    ]

    stations = await get_app_data().controller.get_registered_stations(direction=StationsDirection.TO_MOSCOW)
    stations_names = [station[0] for station in stations]
    text = "Станции в Москву:\n" + "\n".join(stations_names)

    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return REGISTERED_STATIONS_TO_MOSCOW


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(MAIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text('Вы выбрали расписание.', reply_markup=keyboard)
    return SCHEDULE


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.answer()
    await update.callback_query.edit_message_text("ОК, пока!")
    return ConversationHandler.END


def start_bot() -> None:
    """Run the bot."""
    application = Application.builder().token(settings.BOT_TOKEN).build()

    main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(schedule, pattern="^" + str(SCHEDULE) + "$")

            ],
            ADMIN: [
                CallbackQueryHandler(register_station, pattern="^" + str(ADD_STATION) + "$"),
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$"),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ],
            REGISTER_STATION: [
                CallbackQueryHandler(register_station_from_moscow, pattern="^" + str(REGISTER_STATION_FROM_MOSCOW) + "$"),
                CallbackQueryHandler(add_station_to_moscow, pattern="^" + str(ADD_TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$")
            ],
            MY_STATIONS: [
                CallbackQueryHandler(from_moscow, pattern="^" + str(FROM_MOSCOW) + "$"),
                CallbackQueryHandler(to_moscow, pattern="^" + str(TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$")
            ],
            REGISTER_STATION_FROM_MOSCOW: [
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$")
            ],
            TO_MOSCOW: [
                CallbackQueryHandler(my_stations, pattern="^" + str(MY_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$")
            ],
            SCHEDULE: [
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    application.add_handler(main_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    start_bot()