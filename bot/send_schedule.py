import datetime
from core.send_schedule import BaseDataConstructor
from telegram import Update
from telegram.ext import ContextTypes
from core.http_client.http_client import HTTPApiBaseClient
from logger import logger
import settings


class DataConstructor(BaseDataConstructor):
    
    API_KEY = settings.API_KEY
    STATION_DEPARTURE_JELDOR = "s9601675"
    STATION_DEPARTURE_NIJA = "s9601835"
    DATE = "2023-09-23"

    
    def request_schedule(self):
        data = HTTPApiBaseClient(
            domain=settings.API_DOMAIN
        ).make_get_request(
            path="/v3.0/search/",
            params={
                "apikey": self.API_KEY,
                "format": "json",
                "from": self.STATION_DEPARTURE_JELDOR,
                "to": self.STATION_DEPARTURE_NIJA,
                "lang": "ru_RU",
                "page": 1,
                "date": self.DATE,
            },
        )
        return data
    
    def clean_schedule(self, data):
        data = data["segments"]
        result_data = {}
        for item in data[:settings.PAGINATION]:
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

    def constructor(self, data: dict) -> str:
        schedule_message = f"Ваше расписание:\n\n"
        for key, value in data.items():
            train_type = value["type"]
            fulling = value["name"]
            time = value["time"]
            duration = value["duration"]
            platform = value["platform"]
            bold_flag = value["bold_flag"]
            if bold_flag:
                schedule_message += (f"\n\n<b>{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл.</b>\n")
            else:
                schedule_message += (f"\n{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл.")
        return schedule_message



async def load_and_sent_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=DataConstructor({}).get_shedule(),
        parse_mode="html"
    )