from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email = page.get_by_test_id("email")
        self.password = page.get_by_test_id("password")
        self.submit = page.get_by_test_id("login-submit")
        self.error = page.get_by_test_id("login-error")

    def open(self):
        self.page.goto("/auth/login")
        return self

    def login(self, email: str, password: str):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def expect_logged_in(self, name: str):
        expect(self.page.get_by_test_id("page-title")).to_have_text("My account")
        expect(self.page.get_by_test_id("nav-menu")).to_contain_text(name)