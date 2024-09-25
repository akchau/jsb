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
        elif value == "экспресс РЭКС" or value == "фирменный экспресс (билеты c указанием мест)":
            clean_value = "🚝"
        return clean_value

    def _construct_string(self, data: dict):
        train_type = self._clean_train_type(data["train_type"])
        fulling = self._clean_fulling(data["name"])
        departure = data["departure"]
        arrival = data["arrival"]
        time = f"{departure}-{arrival}"
        duration = data["duration"]
        platform = data["departure_platform"]
        if duration <= 20:
            bold_flag = True
        else:
            bold_flag = False
        if bold_flag:
            schedule_message = f"\n\n<b>{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл.</b>\n"
        else:
            schedule_message = f"\n{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл."
        return schedule_message

    def constructor(self, data: dict) -> list:
        schedule_message = f"Ваше расписание:\n\n"
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