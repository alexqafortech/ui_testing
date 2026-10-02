import pytest
from playwright.sync_api import expect

from pages.playwright.catalog_page import PlaywrightCatalogPage

@pytest.fixture
def catalog_page(page):
    return PlaywrightCatalogPage(page)

@pytest.mark.catalog
def test_add_to_cart_via_po(catalog_page):
    catalog_page.open()
    catalog_page.add_product_by_name("iPhone 15")
    expect(catalog_page.header.get_cart_count()).not_to_have_text("0")

@pytest.mark.catalog
def test_auth_page_catalog(playwright_catalog_page_auth):
    playwright_catalog_page_auth.open()
    playwright_catalog_page_auth.add_product_by_name("iPhone 15")
    expect(playwright_catalog_page_auth.header.get_cart_count()).not_to_have_text("0")
