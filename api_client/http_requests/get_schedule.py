from datetime import date
from settings import API_DOMAIN, API_PORT, API_KEY
from core.http_requests.http_client import BasicHTTPSlientParamAuthorization
from ..number_request_controller import api_request_permission


class GetScheduleRequest(BasicHTTPSlientParamAuthorization):
    @api_request_permission
    def get_schedule(self, arrived_station: str, departure_station: str) -> list:
        self.set_headers(
            headers={
                "Content-Type": "application/json"
            }
        )
        self.set_params(
            {
                "format": "json",
                "from": self.validate_str(arrived_station),
                "to": self.validate_str(departure_station),
                "lang": "ru_RU",
                "page": 1,
                "date": date.today(),
                "limit": 1000,
            }
        )
        return self.get(
            path="v3.0/search/"
        )

    def parse_response(self, data: dict) -> list[dict]:
        clean_data: dict = self.validate_dict(data)
        result_list = []
        segments: list = self.validate_list(clean_data.get("segments"))
        for segment in segments:
            parse_result = {}
            parse_result["from"] = self.parse(
                data=segment,
                keys=[("from", dict), ("title", dict)]
            )
            parse_result["to"] = self.parse(
                data=segment,
                keys=[("to", dict), ("title", dict)]
            )
            parse_result["departure_platform"] = self.parse(
                data=segment,
                keys=[("departure_platform", dict)]
            )
            result_list.append(parse_result)
        return result_list


def get_schedule() -> list:
    return GetScheduleRequest(
        host=API_DOMAIN,
        port=API_PORT,
        authorization_key="apikey",
        token=API_KEY,
    ).get_schedule(
        arrived_station="s9601675",
        departure_station="s9601835"
    )
