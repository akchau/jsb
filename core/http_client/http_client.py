import requests
from logger import logger

from core.http_client.url_model import SafeBaseUrl

class HTTPApiBaseClient:

    GET = "GET"

    def __init__(self, domain):
        self.domain = domain
        self.remove_headers()

    
    def make_get_request(self, path: str, params={}):
        url = SafeBaseUrl(
            domain=self.domain,
            path=path,
            params=params
        ).clean_url()
        logger.info(f"Зпрос на url {url}")
        response = requests.get(
            url=url
        )
        return response.json()

    def add_authorization(self, data: dict):
        return data

    def remove_headers(self):
        self.headers = {}