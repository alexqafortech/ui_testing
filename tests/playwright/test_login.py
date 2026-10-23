import pytest
from playwright.sync_api import expect

@pytest.mark.auth
def test_login_success(page):
    page.goto("/login")
    # label для полей не связаны
    page.get_by_role("textbox", name="email").fill("test_user@shopmarket.ru")
    page.get_by_role("textbox", name="Ваш пароль").fill("Password123")
    page.get_by_role("button", name="Войти").click()
    expect(page).to_have_url("http://82.146.39.180:3000/")
    expect(page.get_by_text("Алексей Петров")).to_be_visible()

@pytest.mark.auth
def test_login_wrong_password(page):
    page.goto("/login")
    page.get_by_role("textbox", name="email").fill("test_user@shopmarket.ru")
    page.get_by_role("textbox", name="Ваш пароль").fill("WrongPass1")
    page.get_by_role("button", name="Войти").click()
    expect(page).to_have_url("http://82.146.39.180:3000/login")
    expect(page.get_by_text("Неверный")).to_be_visible()

@pytest.mark.auth
def test_login_blocked_user(page):
    page.goto("/login")
    page.get_by_role("textbox", name="email").fill("blocked_user@shopmarket.ru")
    page.get_by_role("textbox", name="Ваш пароль").fill("Password123")
    page.get_by_role("button", name="Войти").click()
    expect(page.get_by_text("Заблокирован")).to_be_visible()

@pytest.mark.auth
def test_login_empty_form_submit(page):
    page.goto("/login")
    page.get_by_role("button", name="Войти").click()

    email_input = page.get_by_role("textbox", name="email")

    expect(email_input).to_have_js_property("validationMessage", "Please fill out this field.")
