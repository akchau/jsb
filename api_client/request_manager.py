
import datetime
from core.http_client.http_client import HTTPApiBaseClient
import settings

class ApiClient(HTTPApiBaseClient):
    pass


class ReseltDataParser:

    def __init__(self, data: dict):
        self.data = data

    def result(self):
        data = self.data["segments"]
        result_data = {}
        for item in data:
            bold_flag = False
            if self.clean_duration(item["duration"]) <= 20:
                bold_flag = True
            key = item["thread"]["number"]
            type = self.clean_type(item["thread"]["transport_subtype"]["title"])
            name = self.clean_name(item["thread"]["title"])
            departure = self.time_formatter(item["departure"])
            arrival = self.time_formatter(item["arrival"])
            duration = self.clean_duration(item["duration"])
            time = f"{departure}-{arrival}"
            platform = self.clean_platform(item["arrival_platform"])
            result_data[key] = {
                "type": type,
                "name": name,
                "time": time,
                "duration": duration, 
                "platform": platform,
                "bold_flag": bold_flag
            }
        return result_data

    
    def time_formatter(self, value: str):
        datetime_obj = datetime.datetime.fromisoformat(value)

        # Извлекаем часы и минуты из объекта datetime
        hours = datetime_obj.hour
        minutes = datetime_obj.minute

        # Формируем строку в формате 'чч:мм'
        formatted_time = f'{hours:02d}:{minutes:02d}'
        return formatted_time

    def clean_type(self, value: str):
        clean_value = value
        if value == "Стандарт плюс":
            clean_value = "🚈"
        elif value == "Пригородный поезд":
            clean_value = "🚂"
        elif value == "экспресс РЭКС" or value == "фирменный экспресс (билеты c указанием мест)":
            clean_value = "🚝"
        return clean_value

    def clean_name(self, value: str):
        if "Железнодорожная" in value:
            return "🍃"
        else:
            return "♨️"

    def clean_platform(self, value: str):
        for sign in value:
            if sign.isdigit():
                return sign
        return value
    
    def clean_duration(self, value: int):
        return int(value // 60)