from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_TIMEOUT = 10

def wait_for_element(browser, locator: tuple, timeout = DEFAULT_TIMEOUT, message: str | None = None):
    try:
        return WebDriverWait(browser, timeout).until(
        EC.visibility_of_element_located(locator))
    except TimeoutException:
        message = message or f"Элемент {locator} не появился за {timeout} секунд"
        raise TimeoutException(message)

def wait_for_clickable(browser, locator: tuple, timeout = DEFAULT_TIMEOUT, message: str | None = None):
    try:
        return WebDriverWait(browser, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    except TimeoutException:
        message = message or f"Элемент {locator} не стал кликабельным за {timeout} секунд"
        raise TimeoutException(message)

def wait_for_invisibility(browser, locator: tuple, timeout = DEFAULT_TIMEOUT, message: str | None = None):
    try:
        return WebDriverWait(browser, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    except TimeoutException:
        message = message or f"Элемент {locator} не исчез за {timeout} секунд"
        raise TimeoutException(message)

def wait_for_url_contains(browser, url_path, timeout = DEFAULT_TIMEOUT):
    try:
        return WebDriverWait(browser, timeout).until(
            EC.url_contains(url_path)
        )
    except TimeoutException:
        raise TimeoutException(f"URL не стал содержать '{url_path}' за {timeout} секунд. Текущий URL: {browser.current_url}")
