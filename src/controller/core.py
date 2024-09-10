from src.controller.controller_types import Station
from src.services.api_client.core import TransportApiClient
from src.services.db_client.core import DbClient


class ScheduleController:

    def __init__(self, api_client: TransportApiClient, entity: DbClient):
        self.__api_client = api_client
        self.__entity = entity

    # def get_schedule(self, arrived_station, departure_station):
    #     self.__api_client.get_schedule(arrived_station, departure_station)

    # def get_arrived_stations(self):
    #     self.__api_client.get_stations()

    def get_all_stations(self):
        thread_uid = self.__api_client.get_schedule_from_station()
        return self.__api_client.get_stations(thread_uid)

    def get_available_for_registration_stations(self):
        all_stations = self.get_all_stations()
        return [station for station in all_stations if station[1] not in self.__entity.get_registered_stations_codes()]

    def register_new_station(self, station_code):
        stations = self.get_all_stations()
        for station in stations:
            if station[1] == station_code:
                print("Целевая станция обнаружена", station)
                self.__entity.register_station(station)
                break

    def get_registered_stations(self):
        return self.__entity.get_registered_stations()
