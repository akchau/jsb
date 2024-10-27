"""
Обработчики для бота
"""
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler

from src.bot.handlers.handler_types import *
from src.bot.handlers.main_menu import main_menu
from src.bot.handlers.admin import (edit_station, register_station_with_direction,
                                    registered_stations_with_direction)
from src.bot.handlers.schedule import arrived_station, departure_station, schedule
from src.bot.handlers.stop import stop


main_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", main_menu)],
        states={
            # ------------------------------------------- ГЛАВНОЕ МЕНЮ -------------------------------------------------
            MAIN_MENU: [
                CallbackQueryHandler(departure_station,
                                     pattern="^" + str(DEPARTURE_STATION) + "$"),
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION) + "$")

            ],
            # -------------------------------------------= ПРИЛОЖЕНИЯ --------------------------------------------------
            # --------------------------------------------- АДМИНКА ----------------------------------------------------
            # ВЫБОР ДЕЙСТВИЯ СО СТАНЦИЕЙ
            EDIT_STATION: [
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION)),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ],
            # ВЫБОР НОВОЙ СТАНЦИИ
            REGISTER_STATION_WITH_DIRECTION: [
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION))
            ],

            # ВЫБОР ЗАРЕГИСТРИРОВАННОЙ СТАНЦИИ ДЛЯ ПЕРЕМЕЩЕНИЯ И УДАЛЕНИЯ
            REGISTERED_STATIONS_WITH_DIRECTION: [
                CallbackQueryHandler(edit_station, pattern="^" + str(EDIT_STATION)),
                CallbackQueryHandler(registered_stations_with_direction,
                                     pattern="^" + str(REGISTERED_STATIONS_WITH_DIRECTION)),
                CallbackQueryHandler(register_station_with_direction,
                                     pattern="^" + str(REGISTER_STATION_WITH_DIRECTION)),
                CallbackQueryHandler(main_menu,
                                     pattern="^" + str(MAIN_MENU) + "$"),
            ],

            # ------------------------------------------ РАСПИСАНИЕ ----------------------------------------------------

            # СТАНЦИЯ ОТПРАВЛЕНИЯ
            DEPARTURE_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(arrived_station, pattern="^" + str(ARRIVED_STATION)),
                CallbackQueryHandler(schedule, pattern="^" + str(SCHEDULE))
            ],

            # СТАНЦИЯ ПРИБЫТИЯ
            ARRIVED_STATION: [
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$"),
                CallbackQueryHandler(departure_station, pattern="^" + str(DEPARTURE_STATION)),
                CallbackQueryHandler(schedule, pattern="^" + str(SCHEDULE))
            ],

            # ОТОБРАЖЕНИЕ С ПАГИНАЦИЕЙ
            SCHEDULE: [
                CallbackQueryHandler(arrived_station, pattern="^" + str(ARRIVED_STATION)),
                CallbackQueryHandler(departure_station, pattern="^" + str(DEPARTURE_STATION)),
                CallbackQueryHandler(main_menu, pattern="^" + str(MAIN_MENU) + "$")
            ]
        },
        fallbacks=[CommandHandler("stop", stop)],
    )
