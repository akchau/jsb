from mongo_db_client import MongoDbTransport

from src.controller.controller_types import Station


class DbClient:

    STATIONS_COLLECTION_NAME = "stations"

    def __init__(self, db_name, db_host, dp_port, db_user, db_password):
        self.__transport = MongoDbTransport(db_name, db_user, db_password, db_host, dp_port)

    def get_registered_stations(self) -> list[Station]:
        return [
            tuple(exist_station["data"])
            for exist_station in self.__transport.get_list(
                collection_name=self.STATIONS_COLLECTION_NAME
            )
        ]

    def register_station(self, station: Station):
        registered_stations = self.get_registered_stations()
        print("Зареганные станции", registered_stations)
        if station not in registered_stations:
            self.__transport.post(self.STATIONS_COLLECTION_NAME, {"data": tuple(station)})

    def get_registered_stations_codes(self) -> list[str]:
        registered_stations = self.get_registered_stations()
        return [
            exist_station[1]
            for exist_station in registered_stations
        ]

