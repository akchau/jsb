
from datetime import date
from core.http_client.http_client import HTTPApiBaseClient
from shedule_manager.number_request_controller import api_request_permission
import settings

API_KEY = settings.API_KEY
API_DOMAIN = "api.rasp.yandex.net"


class ApiClient(HTTPApiBaseClient):
    pass

@api_request_permission
def request_shedule_from_rest_api(departure_station_code, arrived_station_code):
    data = ApiClient(
        domain=API_DOMAIN
    ).make_get_request(
        path="/v3.0/search/",
        params={
            "apikey": API_KEY,
            "format": "json",
            "from": departure_station_code,
            "to": arrived_station_code,
            "lang": "ru_RU",
            "page": 1,
            "date": date.today(),
            "limit": 1000
        },
    )
    return data