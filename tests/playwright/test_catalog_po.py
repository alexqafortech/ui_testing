import pytest
from playwright.sync_api import expect

from pages.playwright.catalog_page import PlaywrightCatalogPage

@pytest.fixture
def catalog_page(page):
    return PlaywrightCatalogPage(page)

@pytest.mark.catalog
def test_login_success_po(catalog_page):
    catalog_page.open()
    catalog_page.add_product_by_name("iPhone 15")
    expect(catalog_page.header.get_cart_count()).to_have_text("1")

@pytest.mark.catalog
def test_auth_page_catalog(playwright_catalog_page_auth):
    playwright_catalog_page_auth.open()
    playwright_catalog_page_auth.add_product_by_name("iPhone 15")
    expect(playwright_catalog_page_auth.header.get_cart_count()).to_have_text("1")
