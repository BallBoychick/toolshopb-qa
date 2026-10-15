from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.names = page.get_by_test_id("product-name")
        self.search_input = page.get_by_test_id("search-query")
        self.search_button = page.get_by_test_id("search-submit")

    def open(self):
        self.page.goto("/")
        expect(self.names.first).to_be_visible()
        return self

    def search(self, text: str):
        self.search_input.fill(text)
        self.search_button.click()
        expect(self.page.get_by_test_id("search-caption")).to_be_visible()

    def open_first_product(self):
        self.names.first.click()