import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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

    driver = webdriver.Chrome(options = options)
    yield driver

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        screenshot_path = screenshots_dir / f"{request.node.name}.png"
        driver.save_screenshot(str(screenshot_path))
        print(f"\nСкриншот сохранён: {screenshot_path}")
    driver.quit()