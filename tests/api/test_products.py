import pytest

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_products_list_matches_schema(api):
    page = api.products()
    assert page.total > 0
    assert page.data and all(p.price > 0 for p in page.data)


def test_search_returns_matching_products(api):
    r = api.request("GET", "/products/search", params={"q": "hammer"})
    assert r.status_code == 200
    names = [p["name"].lower() for p in r.json()["data"]]
    assert names and all("hammer" in n for n in names)


def test_unknown_product_returns_404(api):
    assert api.request("GET", "/products/does-not-exist").status_code == 404
