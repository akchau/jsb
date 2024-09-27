"""
Модуль отрисовки расписания в Telegram.
"""
class DataConstructor:
    """
    Конструктор сообщения с расписанием.
    """

    def __init__(self, pagination):
        self.__pagination = pagination

    @staticmethod
    def _clean_fulling(value: str) -> str:
        """
        Алгоритм проверки загруженности.
        :param value:
        :return:
        """
        if "Железнодорожная" in value:
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

    def _construct_string(self, data: dict):
        """
        Конструктор строки.
        :param data:
        :return:
        """
        train_type = self._clean_train_type(data["train_type"])
        fulling = self._clean_fulling(data["name"])
        departure = data["departure"]
        arrival = data["arrival"]
        time = f"{departure}-{arrival}"
        duration = data["duration"]
        platform = data["departure_platform"]
        bold_flag = duration <= 20  # Simplified condition
        if bold_flag:
            schedule_message = f"\n\n<b>{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл.</b>\n"
        else:
            schedule_message = f"\n{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл."
        return schedule_message

    def constructor(self, data: dict) -> list:
        """
        Конструирование расписания.
        :param data:
        :return:
        """
        schedule_message = "Ваше расписание:\n\n"
        counter = 0
        result_list = []
        for _, value in data.items():
            if counter < self.__pagination:
                counter += 1
                schedule_message += self._construct_string(value)
            else:
                result_list.append(schedule_message)
                schedule_message = self._construct_string(value)
                counter = 1
        result_list.append(schedule_message)
        return result_list


if __name__ == "__main__":
    constructor = DataConstructor(10)
