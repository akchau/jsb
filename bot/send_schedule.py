from telegram import Update
from telegram.ext import ContextTypes

from core.send_schedule import BaseDataConstructor
from api_client.request_manager import ApiClient, ReseltDataParser

from logger import logger
import settings


class DataConstructor(BaseDataConstructor):
    
    API_KEY = settings.API_KEY
    STATION_DEPARTURE_JELDOR = "s9601675"
    STATION_DEPARTURE_NIJA = "s9601835"
    DATE = "2023-09-23"

    
    def request_schedule(self):
        data = ApiClient(
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
    

    def construct_string(self, data: dict):
        train_type = data["type"]
        fulling = data["name"]
        time = data["time"]
        duration = data["duration"]
        platform = data["platform"]
        bold_flag = data["bold_flag"]
        if bold_flag:
            schedule_message = f"\n\n<b>{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл.</b>\n"
        else:
            schedule_message = f"\n{train_type} {time} ({duration}мин. {fulling}) ~{platform}пл."
        return schedule_message

    def clean_schedule(self, data):
        result_data = ReseltDataParser(
            data=data
        ).result()
        return result_data

    def constructor(self, data: dict) -> list:
        schedule_message = f"Ваше расписание:\n\n"
        counter = 0
        result_list = []
        for _, value in data.items():
            if counter < settings.PAGINATION:
                counter += 1
                schedule_message += self.construct_string(value)
            else:
                result_list.append(schedule_message)
                print(result_list)
                schedule_message = self.construct_string(value)
                counter = 1
        result_list.append(schedule_message)
        return result_list



async def load_and_sent_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    schedule = DataConstructor({}).get_shedule()
    for shedule_object in schedule:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=shedule_object,
            parse_mode="html"
        )