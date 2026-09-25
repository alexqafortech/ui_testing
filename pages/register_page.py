from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

class RegisterPage(BasePage):
    PATH = "/register"
    USERNAME_LOCATOR = (By.NAME, "login")
    EMAIL_LOCATOR = (By.NAME, "email")
    PASSWORD_LOCATOR = (By.NAME, "password")
    PASSWORD_CONFIRM_LOCATOR = (By.NAME, "passwordConfirm")
    AGE_LOCATOR = (By.NAME, "age")
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_MESSAGE_LOCATOR = (By.CSS_SELECTOR, "div[id='register-message']")

    def open(self):
        return super().open(self.PATH)

    def register(self, username: str, email: str, password: str, age, confirm: str = None):
        if confirm is None:
            confirm = password

        self.type_text(self.USERNAME_LOCATOR, username)
        self.type_text(self.EMAIL_LOCATOR, email)
        self.type_text(self.PASSWORD_LOCATOR, password)
        self.type_text(self.PASSWORD_CONFIRM_LOCATOR, confirm)
        self.type_text(self.AGE_LOCATOR, age)
        self.click(self.SUBMIT_BUTTON_LOCATOR)

    def get_success_message(self):
        return self.get_text(self.REGISTER_MESSAGE_LOCATOR)

    def get_error_message(self):
        return self.get_text(self.REGISTER_MESSAGE_LOCATOR)

    def is_submit_disabled(self):
        button = self.find(self.SUBMIT_BUTTON_LOCATOR)
        return button.get_attribute("disabled") is not None

    def native(self):
        element = self.find(self.USERNAME_LOCATOR)
        error_message = self.driver.execute_script("return arguments[0].validationMessage;", element)
        return error_message.strip()



