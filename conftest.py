import os
import pytest
import json
import requests
from pathlib import Path

#Playwright imports
from playwright.sync_api import expect
from pages.playwright.base_page import PlaywrightBasePage
from pages.playwright.login_page import PlaywrightLoginPage
from pages.playwright.catalog_page import PlaywrightCatalogPage
from pages.playwright.cart_page import PlaywrightCartPage
from pages.playwright.orders_page import PlaywrightOrdersPage

#Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.register_page import RegisterPage
from pages.admin_page import AdminPage
from pages.cart_page import CartPage
from pages.profile_page import ProfilePage
from pages.orders_page import OrdersPage


BASE_URL = os.getenv("BASE_URL")

def pytest_addoption(parser):
    parser.addoption(
        "--browser-mode",
        action="store",
        default="headless",
        choices = ["headless", "headed"],
        help = "Режим запуска браузера: headless (фон) или headed (с окном)",
    )

@pytest.hookimpl(hookwrapper = True, tryfirst = True)
def pytest_runtest_makereport(item, call):
    """Сохраняет результат каждой фазы теста в атрибут item.rep_<phase>."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

@pytest.fixture(scope = "session")
def base_url():
    return "http://82.146.39.180:3000/"

# Playwright
@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": "http://82.146.39.180:3000/",
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture(scope = "session")
def storage_state_path(browser, tmp_path_factory):
    path = tmp_path_factory.mktemp("auth") / "state.json"
    context = browser.new_context(base_url="http://82.146.39.180:3000")
    page = context.new_page()

    page.goto("/login")
    page.get_by_role("textbox", name="email").fill("test_user@shopmarket.ru")
    page.get_by_role("textbox", name="Ваш пароль").fill("Password123")
    page.get_by_role("button", name="Войти").click()
    expect(page.get_by_text("Алексей Петров")).to_be_visible()

    context.storage_state(path=str(path))
    context.close()
    return str(path)

@pytest.fixture(scope="session")
def storage_state_path_api(playwright, tmp_path_factory):
    path = tmp_path_factory.mktemp("auth") / "state_api.json"
    request_context = playwright.request.new_context(base_url="http://82.146.39.180:3000")

    response = request_context.post("/api/auth/login", data={
        "email": "test_user@shopmarket.ru",
        "password": "Password123",
        "rememberMe": False
    })
    assert response.status == 200

    request_context.storage_state(path=str(path))
    request_context.dispose()
    return str(path)

@pytest.fixture
def authenticated_page(browser, storage_state_path_api):
    context = browser.new_context(
        base_url = "http://82.146.39.180:3000/",
        storage_state = storage_state_path_api,
    )
    page = context.new_page()
    page.goto("/catalog")

    yield page
    context.close()

@pytest.fixture
def playwright_catalog_page_auth(authenticated_page):
    return PlaywrightCatalogPage(authenticated_page)

@pytest.fixture
def playwright_base_page(page):
    return PlaywrightBasePage(page)

@pytest.fixture
def playwright_login_page(page):
    return PlaywrightLoginPage(page)

@pytest.fixture
def playwright_catalog_page(page):
    return PlaywrightCatalogPage(page)

@pytest.fixture
def playwright_cart_page(page):
    return PlaywrightCartPage(page)

@pytest.fixture
def playwright_orders_page(page):
    return PlaywrightOrdersPage(page)


# Selenium
@pytest.fixture
def driver(request):
    """Запускает Chrome перед тестом и закрывает после."""
    options = Options()
    if request.config.getoption("--browser-mode") == "headless":
        options.add_argument("--headless=new")

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=PasswordLeakDetection")
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options = options)
    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        screenshot_path = screenshots_dir / f"{request.node.name}.png"
        driver.save_screenshot(str(screenshot_path))
        print(f"\nСкриншот сохранён: {screenshot_path}")
    driver.quit()

@pytest.fixture
def create_user_with_hard_password(register_page, admin_page, refresh_data_base):
    register_page.open()

    register_page.register(
        username="test_hard_pass",
        email="test_hard_pass@test.com",
        password="HardPassword123!",
        confirm="HardPassword123!",
        age="20"
    )

    admin_page.open()
    admin_page.activate_user()

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture
def main_page(driver):
    return MainPage(driver)

@pytest.fixture
def catalog_page(driver):
    return CatalogPage(driver)

@pytest.fixture
def register_page(driver):
    return RegisterPage(driver)

@pytest.fixture
def admin_page(driver):
    return AdminPage(driver)

@pytest.fixture
def cart_page(driver):
    return CartPage(driver)

@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)

@pytest.fixture
def orders_page(driver):
    return OrdersPage(driver)

@pytest.fixture
def refresh_data_base(admin_page):
    yield
    admin_page.open()
    admin_page.reload_data_base()

@pytest.fixture
def authenticated_driver(driver, create_user_with_hard_password):
    login = LoginPage(driver)
    login.open().login("test_hard_pass@test.com", "HardPassword123!")
    return driver

@pytest.fixture
def catalog_page_auth(authenticated_driver):
    return CatalogPage(authenticated_driver)

@pytest.fixture()
def reset_db():
    yield
    requests.post("http://82.146.39.180:3000/api/admin/reset-db")
