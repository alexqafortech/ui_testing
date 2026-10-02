import pytest
from playwright.sync_api import expect

@pytest.mark.smoke
def test_login_page(page):
    page.goto("/login")
    assert "/login" in page.url
    assert "Вход" in page.title()

@pytest.mark.smoke
def test_catalog_page(page):
    page.goto("/catalog")
    assert page.locator("div[id='products-grid'] > div").count() > 0

@pytest.mark.smoke
def test_cart_page(page):
    page.goto("/cart")
    assert "/cart" in page.url

@pytest.mark.smoke
def test_login_in_account(page):
    page.goto("/login")
    page.fill("input[name='email']", "test_user@shopmarket.ru")
    page.fill("input[name='password']", "Password123")
    page.click("button[id='login-btn']")

    # Через wait_for_url не получается, потому что редирект идёт на главную страницу, у которой url такой же, только
    # без /login
    heading = page.locator("h1")
    expect(heading).to_contain_text("Весенняя")