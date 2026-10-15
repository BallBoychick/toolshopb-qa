# import pytest

# pytestmark = pytest.mark.hybrid


# def test_user_created_via_api_can_login_in_ui(new_user, login_page):
#     login_page.login(new_user["email"], new_user["password"])
#     login_page.expect_logged_in(new_user["first_name"])