import pytest
import uuid
from playwright.sync_api import expect

@pytest.mark.register
def test_register_form_playwright(page):
    page.goto("/register")

    username = f"test_user{uuid.uuid4().hex[:8]}"
    email = f"test_user{uuid.uuid4().hex[:8]}@test.com"
    password = "Password123"
    age = "20"

    page.get_by_role("textbox", name="Латиница, цифры, _").fill(username)
    page.get_by_role("textbox", name="Ваш email").fill(email)
    page.locator("input[name='password']").fill(password)
    page.locator("input[name='passwordConfirm']").fill(password)
    page.locator("input[name='age']").fill(age)

    page.get_by_role("button", name="Зарегистрироваться").click()
    expect(page.get_by_text("Регистрация успешна!")).to_be_visible()

