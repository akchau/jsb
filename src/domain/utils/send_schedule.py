"""
Модуль отрисовки расписания в Telegram.
"""
import datetime


class DataConstructor:
    """
    Конструктор сообщения с расписанием.
    """

    def __init__(self, pagination):
        self.__pagination = pagination

    @staticmethod
    def _clean_fulling(value: str, target_station_one, target_station_two, speed) -> str:
        """
        Алгоритм проверки загруженности.
        :param value:
        :return:
        """
        if target_station_one in value or target_station_two in value or speed:
            return "🍃"
        else:
            return "♨️"

    @staticmethod
    def _clean_train_type(value: str) -> str:
        """
        Отрисовка смайлика для типа поезда.
        :param value: Строка с описанием типа поезда.
        :return:
        """
        clean_value = value
        if value == "Стандарт плюс":
            clean_value = "🚈"
        elif value == "Пригородный поезд":
            clean_value = "🚂"
        elif value in ["экспресс РЭКС", "фирменный экспресс (билеты c указанием мест)"]:
            clean_value = "🚝"
        return clean_value

    def _construct_string(self, string_tuple: tuple, regular_duration: int, target_station_one, target_station_two):
        """
        Конструктор строки.
        :param data:
        :return:
        """
        title, arrived_time, departure_time, duration, platform, arrival_platform, stops, train_type, _ = string_tuple
        train_type = self._clean_train_type(train_type)

        clean_departure_time = departure_time.strftime("%H:%M")
        clean_arrived_time = arrived_time.strftime("%H:%M")
        time = f"{clean_departure_time}-{clean_arrived_time}"
        bold_flag = duration / regular_duration <= 0.85

        fulling = self._clean_fulling(title, target_station_one=target_station_one, target_station_two=target_station_two,
                                      speed=bold_flag)
        schedule_message = None
        # TODO оно вечером ничего не отдает
        # if datetime.datetime.now().time().hour < int(clean_departure_time.split(":")[0]):
        if bold_flag:
            schedule_message = f"\n<b>{train_type} {time} ({int(duration)}мин. {fulling}) ~{platform}.</b>"
        else:
            schedule_message = f"\n{train_type} {time} ({int(duration)}мин. {fulling}) ~{platform}"
        return schedule_message if schedule_message is not None else ""

    def constructor(self, data: list[tuple], target_station_one, target_station_two) -> list:
        """
        Конструирование расписания.
        :param data:
        :return:
        """
        schedule_message = "Ваше расписание:\n\n"
        counter = 0
        result_list = []
        regular_duration = round(sum([int(obj[3]) for obj in data])/len(data))
        for value in data:
            if counter < self.__pagination:
                counter += 1
                schedule_message += self._construct_string(value, regular_duration, target_station_one, target_station_two)
            else:
                result_list.append(schedule_message)
                schedule_message = self._construct_string(value, regular_duration, target_station_one, target_station_two)
                counter = 1
        result_list.append(schedule_message)
        return result_list


if __name__ == "__main__":
    constructor = DataConstructor(10)
