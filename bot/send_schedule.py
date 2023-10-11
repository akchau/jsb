from telegram import Update
from telegram.ext import ContextTypes

from core.send_schedule import BaseDataConstructor
import settings
from shedule_manager.schedule_getter import get_current_shedule

class DataConstructor(BaseDataConstructor):

    def _request_schedule(self, departure_station_code, arrived_station_code):
        return get_current_shedule(departure_station_code, arrived_station_code)
    
    def _clean_fulling(self, value: str):
        if "Железнодорожная" in value:
            return "🍃"
        else:
            return "♨️"

    def _clean_train_type(self, value: str):
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
            if counter < settings.PAGINATION:
                counter += 1
                schedule_message += self._construct_string(value)
            else:
                result_list.append(schedule_message)
                schedule_message = self._construct_string(value)
                counter = 1
        result_list.append(schedule_message)
        return result_list

async def load_and_sent_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, buttons, departure_station_code, arrived_station_code):
    schedule = DataConstructor({}).get_shedule(departure_station_code, arrived_station_code)
    for shedule_object in schedule:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=shedule_object,
            reply_markup=buttons,
            parse_mode="html"
        )