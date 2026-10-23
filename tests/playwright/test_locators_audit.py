import pytest
from playwright.sync_api import expect

def test_login_page_locators_audit(page):
    page.goto("/login")
    expect(page.get_by_role("textbox", name="email")).to_be_visible()
    expect(page.locator("input[name='password']")).to_be_visible()
    expect(page.locator("#login-btn")).to_be_visible()

def test_header_locators_audit(page):
    page.goto("/login")
    expect(page.locator("a[href='/catalog']")).to_be_visible()

def test_catalog_page_locators_audit(page):
    page.goto("/catalog")
    expect(page.get_by_role("button", name="В корзину").first).to_be_visible()


