from datetime import date
from core.dict_manager.dict_manager import validate_dict
from settings import API_DOMAIN, API_PORT, API_KEY
from core.http_requests.http_client import BasicHTTPClient
from ..number_request_controller import api_request_permission


class GetScheduleRequest(BasicHTTPClient):
    @api_request_permission
    def get_schedule(self, arrived_station: str, departure_station: str) -> list:
        self.set_headers(
            headers={
                "Content-Type": "application/json"
            }
        )
        print(API_KEY)
        self.append_params(
            key="apikey",
            value=API_KEY,
        )
        self.append_params(
            key="format",
            value="json",
        )
        self.append_params(
            key="from",
            value=arrived_station,
        )
        self.append_params(
            key="to",
            value=departure_station,
        )
        self.append_params(
            key="lang",
            value="ru_RU",
        )
        self.append_params(
            key="page",
            value=1,
        )
        self.append_params(
            key="date",
            value=date.today(),
        )
        self.append_params(
            key="limit",
            value=1000,
        )
        return self.get(
            path="v3.0/search/"
        )

    def parse_response(self, data: dict) -> dict:
        clean_data = validate_dict(data)
        print(clean_data)
        return clean_data


def get_schedule():
    print(API_DOMAIN)
    print(API_PORT)
    return validate_dict(
        GetScheduleRequest(
            host=API_DOMAIN,
            port=API_PORT
        ).get_schedule(
            arrived_station="s9601675",
            departure_station="s9601835"

        )
    )
