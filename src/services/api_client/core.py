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
        )

    # def get_stations(self):
    #     self.transport.get(
    #         path="thread/",
    #         headers={
    #             "Content-Type": "application/json"
    #         },
    #         params={
    #             "apikey": self.store["api_key"],
    #             "uid":
    #         }
    #     )

    # def get_schedule(self):
