from typing import Union


class SafeBaseUrl:

    SAFE_PREFIX = "https://"

    def __init__(self, domain: str, path: str, params: dict = {}):
        self.domain = domain
        self.path = path
        self.params = params

    def slice(self, value: str) -> str:
        value = value.strip()
        if value.startswith("/"):
            value = value[1:]
        if value.endswith("/"):
            value = value[:-1]
        return value

    def clean_host(self, domain: str) -> str:
        return f"{self.SAFE_PREFIX}{self.slice(domain)}/"

    def clean_path(self, path: str) -> str:
        return f"{self.slice(path)}/"

    def clean_params(self, params: dict) -> str:
        clean_params = "?"
        for key, value in params.items():
            clean_params = f"{clean_params}{key}={value}&"
        clean_params = clean_params[:-1]
        return clean_params
    
    def clean_url(self):
        return (
            self.clean_host(domain=self.domain) +
            self.clean_path(path=self.path) +
            self.clean_params(params=self.params)
        )