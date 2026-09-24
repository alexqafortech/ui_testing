import pytest
from pathlib import Path
from helpers.waits import wait_for_clickable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
def create_user_with_hard_password(browser):
    browser.get("http://82.146.39.180:3000/register")

    username = "test_hard_pass"
    email = "test_hard_pass@test.com"
    password = "HardPassword123!"
    confirm = "HardPassword123!"
    age = "20"

    username_locator = (By.NAME, "login")
    email_locator = (By.NAME, "email")
    password_locator = (By.NAME, "password")
    password_confirm_locator = (By.NAME, "passwordConfirm")
    age_locator = (By.NAME, "age")
    submit_button_locator = (By.CSS_SELECTOR, "button[type='submit']")

    for locator, value in [
        (username_locator, username),
        (email_locator, email),
        (password_locator, password),
        (password_confirm_locator, confirm),
        (age_locator, age),
    ]:
        input_field = browser.find_element(*locator)
        input_field.clear()
        input_field.send_keys(value)

    wait_for_clickable(browser, submit_button_locator).click()

    browser.get("http://82.146.39.180:3000/admin")
    wait_for_clickable(browser, (By.XPATH, "//td[contains(text(), 'test_hard_pass')]/following-sibling::td[5]/div/button[contains(text(), 'Активировать')]")).click()

@pytest.fixture
def refresh_data_base(browser):
    yield

    try:
        browser.get("http://82.146.39.180:3000/admin")
        wait_for_clickable(browser, (By.ID, "reset-db-btn")).click()
        WebDriverWait(browser, 3).until(EC.alert_is_present())
        browser.switch_to.alert.accept()
    except Exception:
        pass

