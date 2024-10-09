"""
Обработчики для бота
"""
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler

from src.bot.handlers.handler_types import *
from src.bot.handlers.edit_station import edit_station
from src.bot.handlers.main_menu import main_menu, admin
from src.bot.handlers.register_stations import register_station, register_station_with_direction
from src.bot.handlers.registered_stations import registered_stations, registered_stations_with_direction
from src.bot.handlers.schedule import arrived_station, departure_station, schedule_view
from src.bot.handlers.stop import stop


main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={

            # ГЛАВНОЕ МЕНЮ
            MAIN_MENU: [
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(departure_station, pattern="^" + str(DEPARTURE_STATION) + "$")

            ],

            # МЕНЮ АДМИНКИ
            ADMIN: [

                # ПЕРЕХОД К ВЫБОРУ НАПРАВЛЕНИЯ РЕГИСТРАЦИИ СТАНЦИИ
                CallbackQueryHandler(register_station, pattern="^" + str(REGISTER_STATION) + "$"),
                CallbackQueryHandler(registered_stations, pattern="^" + str(REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ],

            # ВЫБОР НАПРАВЛЕНИЯ РЕГИСТРАЦИИ СТАНЦИИ
            REGISTER_STATION: [
                CallbackQueryHandler(register_station_with_direction,
                                     pattern="^" + str(REGISTER_STATION_WITH_DIRECTION)),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
            ],

            # ВЫБОР НАПРАВЛЕНИЯ ЗАРЕГЕСТРИРОВАННЫХ СТАНЦИЙ
            REGISTERED_STATIONS: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION)),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
            ],

            # ВЫБОР НОВОЙ СТАНЦИИ
            REGISTER_STATION_WITH_DIRECTION: [
                CallbackQueryHandler(register_station,
                                     pattern="^" + str(REGISTER_STATION) + "$"),
                CallbackQueryHandler(admin,
                                     pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION))
            ],

            # ВЫБОР ЗАРЕГИСТРИРОВАННОЙ СТАНЦИИ ДЛЯ ПЕРЕМЕЩЕНИЯ И УДАЛЕНИЯ
            REGISTERED_STATIONS_WITH_DIRECTION: [
                CallbackQueryHandler(edit_station, pattern="^" + str(EDIT_STATION)),
                CallbackQueryHandler(register_station_with_direction,
                                     pattern="^" + str(REGISTER_STATION_WITH_DIRECTION)),
                CallbackQueryHandler(registered_stations, pattern="^" + str(REGISTERED_STATIONS) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$"),
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
            ],


            # СТАНЦИЯ ОТПРАВЛЕНИЯ
            DEPARTURE_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(arrived_station, pattern="^" + str(ARRIVED_STATION)),
                CallbackQueryHandler(schedule_view, pattern="^" + str(SCHEDULE_VIEW))
            ],
            # ВЫБОР ДЕЙСТВИЯ СО СТАНЦИЕЙ
            EDIT_STATION: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION)),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(admin, pattern="^" + str(ADMIN) + "$"),
            ],

            # СТАНЦИЯ ПРИБЫТИЯ
            ARRIVED_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(schedule_view, pattern="^" + str(SCHEDULE_VIEW)),
                CallbackQueryHandler(departure_station, pattern="^" + str(DEPARTURE_STATION))
            ],

            # ОТОБРАЖЕНИЕ С ПАГИНАЦИЕЙ
            SCHEDULE_VIEW: [
                CallbackQueryHandler(arrived_station, pattern="^" + str(ARRIVED_STATION)),
                CallbackQueryHandler(departure_station, pattern="^" + str(DEPARTURE_STATION)),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )