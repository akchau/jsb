
from core.json_manager import BaseJsonController, load_dict_in_json
from core.file_manger import delete_file
from api_client.yandex_shedule_client import request_shedule_from_rest_api
from logger import logger
import settings
from shedule_manager.shedule_parser import ScheduleParser, parse_shedule


def get_shedule_key(departure_station_code, arrived_station_code):
    return f"{departure_station_code}-{arrived_station_code}"


class ScheduleSaver(BaseJsonController):

    def _parse_schedule(self, data):
        return parse_shedule(data=data)

    def _save_schedule(self, key, data, filepath):
        delete_file(filepath=filepath)
        load_dict_in_json(
            filepath=filepath,
            data=data
        )

    def _request_shedule(self, departure_station_code, arrived_station_code):
        return request_shedule_from_rest_api(departure_station_code, arrived_station_code)

    def refresh(self, departure_station_code, arrived_station_code):
        data = self._request_shedule(
            departure_station_code=departure_station_code,
            arrived_station_code=arrived_station_code
        )
        clean_data = self._parse_schedule(data=data)
        filepath = self._create_new_filepath(get_shedule_key(departure_station_code, arrived_station_code))
        self._save_schedule(
            key=get_shedule_key(departure_station_code, arrived_station_code),
            data=clean_data,
            filepath=filepath
        )
        self._write_json_record(
            filepath=self.LIST_OF_FILENAMES,
            key=get_shedule_key(departure_station_code, arrived_station_code),
            value=filepath
        )


def refresh_schedule():
    saver = ScheduleSaver()
    for station_tuple in settings.STATIONS:
        arrived_station = station_tuple[0]["code"]
        depatrure_station = station_tuple[1]["code"]
        logger.info(f"ОБНОВЛЯЕМ РАСПСИАНИЕ ДЛЯ {arrived_station}-{depatrure_station}")
        saver.refresh(
            departure_station_code=depatrure_station,
            arrived_station_code=arrived_station
        )

        arrived_station = station_tuple[1]["code"]
        depatrure_station = station_tuple[0]["code"]
        logger.info(f"ОБНОВЛЯЕМ РАСПСИАНИЕ ДЛЯ {arrived_station}-{depatrure_station}")
        saver.refresh(
            departure_station_code=depatrure_station,
            arrived_station_code=arrived_station
        )

