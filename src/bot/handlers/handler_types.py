from typing import Optional

from pydantic import BaseModel


(MAIN_MENU, ADMIN, REGISTER_STATION, REGISTER_STATION_WITH_DIRECTION,
 REGISTERED_STATIONS, REGISTERED_STATIONS_WITH_DIRECTION, DEPARTURE_STATION, ARRIVED_STATION,
 EDIT_STATION, SCHEDULE_VIEW) = range(10)


class MenuSection(BaseModel):
    title: str
    back_to_title: Optional[str] = "Неизвестное значение"


class MenuSections:
    main_menu = MenuSection(title='Главное меню 🔢', back_to_title='⬅️ Главное меню 🔢')
    admin_zone = MenuSection(title='Админка 🔴️️', back_to_title='⬅️ Главное меню администартора 🔴️️')
    schedule = MenuSection(title="Расписание 📅", back_to_title="⬅️ Расписание 📅")
    my_stations = MenuSection(title="Мои станции 🛤", back_to_title="️⬅️ к выбору направления")
    departure_station = MenuSection(title="Станция отправления", back_to_title="🔁 станцию отправления")
    arrived_station = MenuSection(title="Станция прибытия", back_to_title="🔁 станцию прибытия")
    register_station = MenuSection(title="Новая станция 🆕", back_to_title="️⬅️ к выбору направления")
    delete = MenuSection(title="Удалить ❌")
    move = MenuSection(title="Переместить 🔁")
    register_station_with_direction_to_moscow = MenuSection(title="В Москву 🏢🚄🏡",
                                                              back_to_title="Зарегистрировать 🆕")
    register_station_with_direction_from_moscow = MenuSection(title="Из Москвы 🏡🚄🏢",
                                                              back_to_title="Зарегистрировать 🆕")
    registered_station_with_direction_to_moscow = MenuSection(title="В Москву 🏢🚄🏡",
                                                            back_to_title="Мои станции 🛤")
    registered_station_with_direction_from_moscow = MenuSection(title="Из Москвы 🏡🚄🏢",
                                                              back_to_title="Мои станции 🛤")


