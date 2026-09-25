from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class LoginPage(BasePage):

    EMAIL_INPUT = (By.CSS_SELECTOR, '[name="email"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, '[type="password"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, '[type="submit"]')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.error-message-container')
    USER_NAME = (By.CSS_SELECTOR, "div[class='relative group'] button:first-child")
    PARAM_1 = (By.NAME, "email")
    PATH = "/login"

    def open(self):
        return super().open(self.PATH)

    def login(self, email, password):
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

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