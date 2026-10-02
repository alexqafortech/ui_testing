Selenium login_page:
```
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from components.header import HeaderComponent
from pages.main_page import MainPage

class LoginPage(BasePage):

    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[type="password"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error-message-container')
    USER_NAME = (By.CSS_SELECTOR, "div[class='relative group'] button:first-child")
    PARAM_1 = (By.NAME, "email")
    PATH = "/login"

    def __init__(self, driver, base_url = None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    def open(self):
        return super().open(self.PATH)

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)
        main = MainPage(self.driver)
        main.wait_for_url_contains("/")
        return main

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def get_logged_in_user(self) -> str:
        # Из-за того-что нет редиректа на /accounts может падать
        #self.wait_for_url_contains("")
        return self.get_text(self.USER_NAME)

    def is_login_form_loaded(self) -> bool:
        return (
                self.is_visible(self.EMAIL_INPUT)
                and self.is_visible(self.PASSWORD_INPUT)
                and self.is_visible(self.SUBMIT_BUTTON)
        )
```

Playwright login_page:
```
from pages.playwright.base_page import PlaywrightBasePage

class PlaywrightLoginPage(PlaywrightBasePage):
    PATH = "/login"

    def __init__(self, page, base_url = None):
        super().__init__(page)

        self.email = page.get_by_role("textbox", name="email")
        self.password = page.get_by_role("textbox", name="Ваш пароль")
        self.submit = page.get_by_role("button", name="Войти")
        self.error = page.get_by_text("Неверный")
        self.block_error = page.get_by_text("Заблокирован")
        self.user_name = page.locator("div[class='relative group']>button")

    def open(self):
        self.navigate(self.PATH)
        return self

    def login(self, email: str | None, password: str | None):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()

    def get_error(self):
        return self.error

    def get_username(self):
        return self.user_name

    def click_submit(self):
        self.submit.click()

    def get_email(self):
        return self.email

```

Selenium base_page:
```
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

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
        element.send_keys(Keys.CONTROL + "a")
        element.send_keys(Keys.BACKSPACE)
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

```

Playwright base_page:
```
class PlaywrightBasePage:

    def __init__(self, page, base_url: str="http://82.146.39.180:3000"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path=""):
        self.page.goto(self.base_url + path)
        return self

    def get_title(self):
        return self.page.title()

    def current_url(self):
        return self.page.url

    def screenshot(self, path):
        self.page.screenshot(path=path)

```

Таблица различий:

|              | Selenium | Playwright |
|:-------------| :--- | :--- |
| **Локаторы** | XPATH, CSS_SELECTOR, By.ID/name | by_role, by_text, by_label, by_placeholder, by_test_id, CSS_SELECTOR |
| **Ожидания** | Прописываются вручную | Встроены в методы |
| **Геттеры**  | Длинные, необходимы дополнительные ожидания, при обновлении страницы устаревает | Возвращают объект локатора, который описывает, как найти элемент |
| **Проверки** | Через assert, необходимы дополнительные ожидания | Через expect, ожидания уже встроены |

Что осталось одинаковым:
Page object не зависит, от того, при помощи какого инструменты, мы его реализуем. Единственное различие, что реализация на Playwright оказывается тоньше, из-за того, что не надо добавлять дополнительные ожидания, локаторы не протухают

Playwright PO экономит время, путем уменьшения времени на его изучения, из-за того, что PO короток и лаконичен, его можно быстрее изучить.  