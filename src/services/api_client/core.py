from api_client import ApiClient


class TransportApiClient(ApiClient):

    def get_schedule_from_station(self):
        return self.transport.get(
            path="schedule/",
            headers={
                "Content-Type": "application/json"
            },
            params={
                "apikey": self.store["api_key"],
                "station": "s9601675",
                "transport_types": "suburban"
            }
        )["schedule"][0]["thread"]["uid"]

    def get_stations(self, thread_uid):
        all_stations_data = self.transport.get(
            path="thread/",
            headers={
                "Content-Type": "application/json"
            },
            params={
                "apikey": self.store["api_key"],
                "uid": thread_uid
            }
        )["stops"]
        return [(station["station"]["title"], station["station"]["code"]) for station in all_stations_data]

    # def get_schedule(self):
