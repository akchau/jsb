
from core.json_manager import BaseJsonController
from shedule_manager.schedule_saver import get_shedule_key


class ScheduleGetter(BaseJsonController):

    def get_shedule(self, departure_station_code, arrived_station_code):
        key = get_shedule_key(departure_station_code, arrived_station_code)
        filepath = self._get_json_record(
            filepath=self.LIST_OF_FILENAMES,
            key=key
        )
        return BaseJsonController.read_dict_in_json(filepath=filepath)

def get_current_shedule(departure_station_code, arrived_station_code):
    return ScheduleGetter().get_shedule(departure_station_code, arrived_station_code)