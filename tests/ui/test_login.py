import pytest
from src.config import CUSTOMER

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_customer_can_login(login_page):
    login_page.login(**CUSTOMER)
    login_page.expect_logged_in("Jane Doe")


def test_login_with_wrong_password_shows_error(login_page):
    login_page.login(CUSTOMER["email"], "wrong-password")
    login_page.error.wait_for()
    assert "Invalid" in login_page.error.inner_text()