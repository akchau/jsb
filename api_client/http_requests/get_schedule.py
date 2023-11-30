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
        self.append_params_in_dict(
            {
                "apikey": API_KEY,
                "format": "json",
                "from": arrived_station,
                "to": departure_station,
                "lang": "ru_RU",
                "page": 1,
                "date": date.today(),
                "limit": 1000,
            }
        )
        return self.get(
            path="v3.0/search/"
        )

    def parse_from_station(self, segment_data: dict[str]) -> str:
        from_station_data = validate_dict(segment_data.get("from"))
        return from_station_data.get("title")

    def parse_to_station(self, segment_data: dict[str]) -> str:
        to_station_data = validate_dict(segment_data.get("to"))
        return to_station_data.get("title")

    def parse_departure_platform(self, segment_data: dict[str]) -> str:
        print(segment_data)
        return segment_data.get("departure_platform")

    def parse_response(self, data: dict) -> list[dict]:
        clean_data: dict = validate_dict(data)
        # print(clean_data.keys())
        # print(clean_data.get("search"))
        result_list = []
        segments: list = clean_data.get("segments")
        for segment in segments:
            parse_result = {}
            clean_segment = validate_dict(segment)
            # print(clean_segment.keys())
            parse_result["from"] = self.parse_from_station(
                segment_data=clean_segment
            )
            parse_result["to"] = self.parse_to_station(
                segment_data=clean_segment
            )
            parse_result["departure_platform"] = self.parse_departure_platform(
                segment_data=clean_segment
            )
            result_list.append(parse_result)
        return result_list


def get_schedule() -> list:
    return validate_dict(
        GetScheduleRequest(
            host=API_DOMAIN,
            port=API_PORT
        ).get_schedule(
            arrived_station="s9601675",
            departure_station="s9601835"
        )
    )
