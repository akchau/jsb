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
from src.bot.handlers.schedule import arrived_station, departure_station, schedule_view
from src.bot.handlers.stop import stop

main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={

            # ГЛАВНОЕ МЕНЮ
            constants.MAIN_MENU: [
                CallbackQueryHandler(admin, pattern="^" + str(constants.ADMIN) + "$"),
                CallbackQueryHandler(departure_station, pattern="^" + str(constants.DEPARTURE_STATION) + "$")

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


            # СТАНЦИЯ ОТПРАВЛЕНИЯ
            constants.DEPARTURE_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$"),
                CallbackQueryHandler(arrived_station, pattern="^" + str(constants.ARRIVED_STATION))
            ],
            # ВЫБОР ДЕЙСТВИЯ СО СТАНЦИЕЙ
            constants.EDIT_STATION: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(constants.REGISTERED_STATIONS_WITH_DIRECTION))
            ],

            # СТАНЦИЯ ПРИБЫТИЯ
            constants.ARRIVED_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$"),
                CallbackQueryHandler(schedule_view, pattern="^" + str(constants.SCHEDULE_VIEW)),
                CallbackQueryHandler(departure_station, pattern="^" + str(constants.DEPARTURE_STATION))
            ],

            # ОТОБРАЖЕНИЕ С ПАГИНАЦИЕЙ
            constants.SCHEDULE_VIEW: [
                CallbackQueryHandler(arrived_station, pattern="^" + str(constants.ARRIVED_STATION)),
                CallbackQueryHandler(departure_station, pattern="^" + str(constants.DEPARTURE_STATION)),
                CallbackQueryHandler(main_menu, pattern="^" + str(constants.MAIN_MENU) + "$")
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )
