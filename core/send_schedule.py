from core.json_manager import load_dict_in_json, read_json
from logger import logger

class BaseDataConstructor:

    def __init__(self, input_params: dict) -> None:
        self._input_params: dict = input_params

    def _request_schedule(self) -> dict:
        data = {}
        return data

    def _clean_schedule(self, data: dict) -> dict:
        return data

    def _validate_schedule(self, data) -> dict:
        return data

    def constructor(self, data: dict) -> list:
        schedule_message = f"Ваше расписание:\n\n{data}"
        return schedule_message

    def _construct_schedule(self, departure_station_code, arrived_station_code) -> list:
        schedule = self._request_schedule(departure_station_code, arrived_station_code)
        clean_schedule = self._clean_schedule(data=schedule)
        valide_scheule = self._validate_schedule(data=clean_schedule)
        return self.constructor(data=valide_scheule)

    def get_shedule(self, departure_station_code, arrived_station_code) -> str:
        logger.info(f'Получен запрос на загрузку расписания с {self._input_params}')
        return self._construct_schedule(departure_station_code, arrived_station_code)
