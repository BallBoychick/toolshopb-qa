import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_search_shows_only_matching_products(catalog):
    catalog.search("hammer")
    expect(catalog.names.first).to_be_visible()
    for name in catalog.names.all_inner_texts():
        assert "hammer" in name.lower()


@pytest.mark.smoke
def test_add_product_to_cart(catalog, page):
    catalog.open_first_product()
    page.get_by_test_id("add-to-cart").click()
    expect(page.get_by_test_id("cart-quantity")).to_have_text("1")