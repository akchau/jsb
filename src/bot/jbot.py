import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

from src.settings import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define states
SELECTING_ACTION, ADMIN_MENU, SCHEDULE, ADD_STATION, MY_STATIONS = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display a menu with choices for the user."""
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
    """Display admin submenu."""
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
    """Handle the add station button."""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали добавить станцию.", reply_markup=keyboard)
    return ADD_STATION


async def my_stations(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the my stations button."""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(ADMIN_MENU))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали мои станции.", reply_markup=keyboard)
    return MY_STATIONS


async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the schedule button."""
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data=str(SELECTING_ACTION))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text="Вы выбрали расписание.", reply_markup=keyboard)
    return SCHEDULE


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""
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
            MY_STATIONS: [
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN_MENU) + "$")
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