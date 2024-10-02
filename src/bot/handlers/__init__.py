"""
Обработчики для бота
"""
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler

from src.bot import constants
from src.bot.handlers.admin import admin
from src.bot.handlers.edit_station import edit_station
from src.bot.handlers.main_menu import main_menu
from src.bot.handlers.register_stations import register_station, register_station_with_direction
from src.bot.handlers.registered_stations import registered_stations, registered_stations_with_direction
from src.bot.handlers.schedule import schedule
from src.bot.handlers.stop import stop

main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={

            # ГЛАВНОЕ МЕНЮ
            constants.MAIN_MENU: [
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$"),
                CallbackQueryHandler(schedule, pattern="^" + str(constants.SCHEDULE) + "$")

            ],

            # МЕНЮ АДМИНКИ
            constants.ADMIN: [

                # ПЕРЕХОД К ВЫБОРУ НАПРАВЛЕНИЯ РЕГИСТРАЦИИ СТАНЦИИ
                CallbackQueryHandler(register_station, pattern="^" + str(constants.REGISTER_STATION) + "$"),
                CallbackQueryHandler(registered_stations, pattern="^" + str(constants.REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$")
            ],

            # ВЫБОР НАПРАВЛЕНИЯ РЕГИСТРАЦИИ СТАНЦИИ
            constants.REGISTER_STATION: [
                CallbackQueryHandler(register_station_with_direction,
                                     pattern="^" + str(constants.REGISTER_STATION_WITH_DIRECTION)),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(constants.ADMIN) + "$")
            ],

            # ВЫБОР НАПРАВЛЕНИЯ ЗАРЕГЕСТРИРОВАННЫХ СТАНЦИЙ
            constants.REGISTERED_STATIONS: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(constants.REGISTERED_STATIONS_WITH_DIRECTION)),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(constants.ADMIN) + "$")
            ],

            # ВЫБОР НОВОЙ СТАНЦИИ
            constants.REGISTER_STATION_WITH_DIRECTION: [
                CallbackQueryHandler(register_station,
                                     pattern="^" + str(constants.REGISTER_STATION) + "$"),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(constants.ADMIN) + "$"),
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(constants.REGISTERED_STATIONS_WITH_DIRECTION))
            ],

            # ВЫБОР ЗАРЕГИСТРИРОВАННОЙ СТАНЦИИ ДЛЯ ПЕРЕМЕЩЕНИЯ И УДАЛЕНИЯ
            constants.REGISTERED_STATIONS_WITH_DIRECTION: [
                CallbackQueryHandler(edit_station, pattern="^" + str(constants.EDIT_STATION)),
                CallbackQueryHandler(registered_stations, pattern="^" + str(constants.REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$")
            ],

            # ВЫБОР НАПРАВЛЕНИЯ РАСПИСАНИЯ
            constants.SCHEDULE: [
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$")
            ],

            # СТАНЦИЯ ОТПРАВЛЕНИЯ
            constants.DEPARTURE_STATION: [
                CallbackQueryHandler(schedule, pattern="^" + str(constants.SCHEDULE) + "$")
            ],

            # ВЫБОР ДЕЙСТВИЯ СО СТАНЦИЕЙ
            constants.EDIT_STATION: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(constants.REGISTERED_STATIONS_WITH_DIRECTION))
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )
