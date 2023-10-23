from datetime import datetime


class ScheduleParser:

    def __init__(self, data):
        self.data = self.parse_data(data)

    def parse_data(self, data):
        result_data = {}
        segments = data["segments"]
        for item in segments:
            thread_number = item["thread"]["number"]
            duration = self._clean_duration(item["duration"])
            train_type = item["thread"]["transport_subtype"]["title"]
            name = item["thread"]["title"]
            departure = self._time_formatter(item["departure"])
            arrival = self._time_formatter(item["arrival"])
            departure_platform = self._clean_platform(item["departure_platform"])
            result_data[thread_number] = {
                "duration": duration,
                "train_type": train_type,
                "name": name,
                "departure": departure,
                "arrival": arrival,
                "departure_platform": departure_platform
            }
        return result_data

    @property
    def clean_data(self):
        return self.data

    def _clean_platform(self, value: str):
        if isinstance(value, str):
            if value == "":
                return value
            for sign in value:
                if sign.isdigit():
                    return sign
        raise ValueError(f"Неверное значение платформы - {value}")

    def _clean_duration(self, value: int):
        if isinstance(value, int) or (isinstance(value, str) and value.isdigit()) or isinstance(value, float):
            return int(value // 60)
        raise ValueError(f"Неверное значение длительности - {value}")

    def _time_formatter(self, value: str):
        datetime_obj = datetime.fromisoformat(value)

        # Извлекаем часы и минуты из объекта datetime
        hours = datetime_obj.hour
        minutes = datetime_obj.minute

        # Формируем строку в формате 'чч:мм'
        formatted_time = f'{hours:02d}:{minutes:02d}'
        return formatted_time


def parse_shedule(data):
    return ScheduleParser(data=data).clean_data