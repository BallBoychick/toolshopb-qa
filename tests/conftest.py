import uuid
import pytest
from src.config import API_URL, CUSTOMER
from src.api.client import ApiClient
from src.pages.login_page import LoginPage
from src.pages.catalog_page import CatalogPage


@pytest.fixture(scope="session", autouse=True)
def _test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def api() -> ApiClient:
    return ApiClient(API_URL)


@pytest.fixture(scope="session")
def customer_token(api) -> str:
    return api.get_token(**CUSTOMER)


@pytest.fixture
def auth_api(customer_token) -> ApiClient:
    return ApiClient(API_URL, token=customer_token)


@pytest.fixture
def new_user(api) -> dict:
    """Свежий пользователь, созданный через API (данные подготавливаем быстро)."""
    user = {
        "first_name": "Test", "last_name": "User",
        "dob": "1990-01-01", "phone": "123456789",
        "address": {"street": "Main 1", "city": "Frankfurt", "state": "HE",
                    "country": "DE", "postal_code": "60311"},
        "email": f"qa_{uuid.uuid4().hex[:10]}@example.com",
        "password": "Str0ng!Passw0rd#2026",
    }
    r = api.register_user(user)
    assert r.status_code in (200, 201), r.text
    return user


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def catalog(page) -> CatalogPage:
    return CatalogPage(page).open()