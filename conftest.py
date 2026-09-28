import pytest
import requests
from pathlib import Path
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
    return "http://82.146.39.180:3000"

@pytest.fixture
def browser(request):
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
def login_page(browser):
    return LoginPage(browser)

@pytest.fixture
def main_page(browser):
    return MainPage(browser)

@pytest.fixture
def catalog_page(browser):
    return CatalogPage(browser)

@pytest.fixture
def register_page(browser):
    return RegisterPage(browser)

@pytest.fixture
def admin_page(browser):
    return AdminPage(browser)

@pytest.fixture
def cart_page(browser):
    return CartPage(browser)

@pytest.fixture
def profile_page(browser):
    return ProfilePage(browser)

@pytest.fixture
def orders_page(browser):
    return OrdersPage(browser)

@pytest.fixture
def refresh_data_base(admin_page):
    yield
    admin_page.open()
    admin_page.reload_data_base()

@pytest.fixture
def authenticated_driver(browser, create_user_with_hard_password):
    login = LoginPage(browser)
    login.open().login("test_hard_pass@test.com", "HardPassword123!")
    return browser

@pytest.fixture
def catalog_page_auth(authenticated_driver):
    return CatalogPage(authenticated_driver)

@pytest.fixture
def reset_db(base_url):
    requests.post(f"{base_url}/api/admin/reset-db")
    yield
