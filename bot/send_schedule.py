from core.send_schedule import BaseDataConstructor
import logging
from telegram import Update
from telegram.ext import ContextTypes
from core.http_client.http_client import HTTPApiBaseClient
from logger import logger


class DataConstructor(BaseDataConstructor):
    
    YANDEX_API_KEY = "c6f80609-48e8-4583-8a4b-4d1d2175a06a"
    STATION_DEPARTURE_JELDOR = "s9601675"
    STATION_DEPARTURE_NIJA = "s9601835"
    DATE = "2023-09-23"

    
    def request_schedule(self):
        data = HTTPApiBaseClient(
            domain="api.rasp.yandex.net"
        ).make_get_request(
            path="/v3.0/search/",
            params={
                "apikey": self.YANDEX_API_KEY,
                "format": "json",
                "from": self.STATION_DEPARTURE_JELDOR,
                "to": self.STATION_DEPARTURE_NIJA,
                "lang": "ru_RU",
                "page": 1,
                "date": self.DATE,
            },
        )
        return data
    
    def clean_schedule(self, data: dict) -> dict:
        clean_data = data.get("segments")
        return clean_data[0]



async def load_and_sent_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=DataConstructor({}).get_shedule()
    )