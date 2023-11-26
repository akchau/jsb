from settings import API_DOMAIN, API_PORT
from core.http_requests.http_client import BasicHTTPClient
from ..number_request_controller import api_request_permission


class GetScheduleRequest(BasicHTTPClient):
    @api_request_permission
    def get_schedule(self) -> list:
        return self.get(
            path="v3.0/search/"
        )


def get_schedule():
    return GetScheduleRequest(
        host=API_DOMAIN,
        port=API_PORT
    ).get_schedule()
