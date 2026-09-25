from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DEFAULT_TIMEOUT = 10
BASE_URL = "http://82.146.39.180:3000"

class BasePage:
    def __init__(self, driver: WebDriver, base_url: str = BASE_URL):
        self.driver = driver
        self.base_url = base_url

    def open(self, path: str=""):
        self.driver.get(self.base_url + path)
        return self

    def find(self, locator: tuple, timeout=DEFAULT_TIMEOUT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Элемент {locator} не появился за {timeout} секунд"
            )

    def find_clickable(self, locator: tuple, timeout=DEFAULT_TIMEOUT):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            raise TimeoutException(
                f"Элемент {locator} не стал кликабельным за {timeout} секунд"
            )

    def find_all(self, locator: tuple, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple):
        self.find_clickable(locator).click()

    def type_text(self, locator: tuple, text: str):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple):
        return self.find(locator).text

    def is_visible(self, locator: tuple, timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, part: str,timeout=DEFAULT_TIMEOUT):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(part)
            )
        except TimeoutException:
            raise TimeoutException(
                f"URL не стал содержать {part} за {timeout} секунд. Текущий URL {self.driver.current_url}"
            )

    def wait_until(self, condition, timeout=DEFAULT_TIMEOUT):
        try:
            return WebDriverWait(self.driver, timeout).until(condition)
        except TimeoutException:
            raise TimeoutException(
                f"Условие не выполнилось за {timeout} секунд"
            )

    def alert_accept(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            raise TimeoutException(f"Браузерное модальное окно (alert) не появилось за 10 секунд.")

    def refresh(self):
        self.driver.refresh()
        return self
