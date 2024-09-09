class ScheduleController:

    def __init__(self, api_client):
        self.__api_client = api_client

    def get_schedule(self, arrived_station, departure_station):
        self.__api_client.get_schedule(arrived_station, departure_station)

    def get_arrived_stations(self):
        self.__api_client.get_stations()
