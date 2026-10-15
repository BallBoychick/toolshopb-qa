import pytest
from src.config import CUSTOMER

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_returns_token(api):
    r = api.login(**CUSTOMER)
    assert r.status_code == 200
    assert r.json()["access_token"]


@pytest.mark.parametrize("email, password", [
    (CUSTOMER["email"], "wrong-password"),
    ("nobody@example.com", "welcome01"),
])
def test_login_invalid_credentials(api, email, password):
    assert api.login(email, password).status_code == 401


def test_protected_endpoint_requires_token(api):
    assert api.request("GET", "/users/me").status_code == 401


def test_protected_endpoint_with_token(auth_api):
    r = auth_api.request("GET", "/users/me")
    assert r.status_code == 200
    assert r.json()["email"] == "customer@practicesoftwaretesting.com"