from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler

from src.bot import constants
from src.bot.handlers.admin import admin
from src.bot.handlers.main_menu import main_menu
from src.bot.handlers.register_stations import register_station, register_station_from_moscow, \
    register_station_to_moscow
from src.bot.handlers.registered_stations import registered_stations, registered_stations_from_moscow, \
    registered_stations_to_moscow
from src.bot.handlers.schedule import schedule
from src.bot.handlers.stop import stop

main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={
            constants.MAIN_MENU: [
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$"),
                CallbackQueryHandler(schedule, pattern="^" + str(constants.SCHEDULE) + "$")

            ],
            constants.ADMIN: [
                CallbackQueryHandler(register_station, pattern="^" + str(constants.REGISTER_STATION) + "$"),
                CallbackQueryHandler(registered_stations, pattern="^" + str(constants.REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$")
            ],
            constants.REGISTER_STATION: [
                CallbackQueryHandler(register_station_from_moscow, pattern="^" + str(constants.REGISTER_STATION_FROM_MOSCOW) + "$"),
                CallbackQueryHandler(register_station_to_moscow, pattern="^" + str(constants.REGISTER_STATION_TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.REGISTERED_STATIONS: [
                CallbackQueryHandler(registered_stations_from_moscow, pattern="^" + str(constants.REGISTERED_STATIONS_FROM_MOSCOW) + "$"),
                CallbackQueryHandler(registered_stations_to_moscow, pattern="^" + str(constants.REGISTERED_STATIONS_TO_MOSCOW) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.REGISTER_STATION_FROM_MOSCOW: [
                CallbackQueryHandler(register_station, pattern="^" + str(constants.REGISTER_STATION) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.REGISTER_STATION_TO_MOSCOW: [
                CallbackQueryHandler(register_station, pattern="^" + str(constants.REGISTER_STATION) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.REGISTERED_STATIONS_FROM_MOSCOW: [
                CallbackQueryHandler(registered_stations, pattern="^" + str(constants.REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.REGISTERED_STATIONS_TO_MOSCOW: [
                CallbackQueryHandler(registered_stations, pattern="^" + str(constants.REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],
            constants.SCHEDULE: [
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$")
            ],
            constants.DEPARTURE_STATION: [
                CallbackQueryHandler(schedule, pattern="^" + str(constants.SCHEDULE) + "$")
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )