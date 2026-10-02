import pytest
from playwright.sync_api import expect

from pages.playwright.login_page import PlaywrightLoginPage

@pytest.fixture
def login_page(page):
    return PlaywrightLoginPage(page)

@pytest.mark.auth
def test_login_success_po(login_page):
    login_page.open()
    login_page.login("test_user@shopmarket.ru", "Password123")
    username_element = login_page.get_username()
    expect(username_element).to_have_text("Алексей Петров")

@pytest.mark.auth
def test_wrong_password_po(login_page):
    login_page.open()
    login_page.login("test_user@shopmarket.ru", "WrongPass123")
    expect(login_page.error).to_be_visible()

@pytest.mark.auth
def test_empty_form_po(login_page):
    login_page.open()
    login_page.click_submit()

    email = login_page.get_email()

    expect(email).to_have_js_property("validationMessage", "Please fill out this field.")


