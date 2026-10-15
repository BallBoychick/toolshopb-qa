import requests
from src.api.models import ProductPage


class ApiClient:
    def __init__(self, base_url: str, token: str | None = None):
        self.base = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Accept"] = "application/json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        return self.session.request(method, f"{self.base}{path}", timeout=15, **kwargs)

    def login(self, email: str, password: str) -> requests.Response:
        return self.request("POST", "/users/login", json={"email": email, "password": password})

    def get_token(self, email: str, password: str) -> str:
        r = self.login(email, password)
        assert r.status_code == 200, r.text
        return r.json()["access_token"]

    def products(self, **params) -> ProductPage:
        r = self.request("GET", "/products", params=params)
        assert r.status_code == 200, r.text
        return ProductPage(**r.json())

    def register_user(self, payload: dict) -> requests.Response:
        return self.request("POST", "/users/register", json=payload)