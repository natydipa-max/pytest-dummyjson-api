import requests

from src.config import BASE_URL, DEFAULT_TIMEOUT


class BaseClient:

    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

    def get(self, endpoint: str, **kwargs):
        return self.session.get(
            f"{self.base_url}{endpoint}",
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

    def post(self, endpoint: str, **kwargs):
        return self.session.post(
            f"{self.base_url}{endpoint}",
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

    def put(self, endpoint: str, **kwargs):
        return self.session.put(
            f"{self.base_url}{endpoint}",
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

    def delete(self, endpoint: str, **kwargs):
        return self.session.delete(
            f"{self.base_url}{endpoint}",
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )

    def send_raw(self, method: str, endpoint: str, raw_body: str, **kwargs):
        headers = {"Content-Type": "application/json"}
        headers.update(kwargs.pop("headers", {}))

        return self.session.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            data=raw_body,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
            **kwargs,
        )
