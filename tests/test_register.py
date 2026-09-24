import pytest
import uuid
from selenium.webdriver.common.by import By
from helpers.waits import wait_for_element, wait_for_clickable

REGISTER_URL = "/register"
USERNAME_LOCATOR = (By.NAME, "login")
EMAIL_LOCATOR = (By.NAME, "email")
PASSWORD_LOCATOR = (By.NAME, "password")
PASSWORD_CONFIRM_LOCATOR = (By.NAME, "passwordConfirm")
AGE_LOCATOR = (By.NAME, "age")
SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, "button[type='submit']")
REGISTER_MESSAGE_LOCATOR = (By.CSS_SELECTOR, "div[id='register-message']")


def fill_register_form(browser, username: str, email: str, password: str, confirm: str, age: str):
    wait_for_element(browser, USERNAME_LOCATOR)

    for locator, value in [
        (USERNAME_LOCATOR, username),
        (EMAIL_LOCATOR, email),
        (PASSWORD_LOCATOR, password),
        (PASSWORD_CONFIRM_LOCATOR, confirm),
        (AGE_LOCATOR, age),
    ]:
        input_field = browser.find_element(*locator)
        input_field.clear()
        input_field.send_keys(value)

@pytest.mark.register
def test_register_success(browser, base_url):
    browser.get(base_url+REGISTER_URL)

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Password123"
    confirm = "Password123"
    age = "20"

    fill_register_form(browser, username, email, password, confirm, age)

    #Чекбокс согласия не реализован

    wait_for_clickable(browser, SUBMIT_BUTTON_LOCATOR).click()

    message_text = wait_for_element(browser, REGISTER_MESSAGE_LOCATOR).text

    assert "Регистрация успешна! Подтвердите email по ссылке" in message_text

@pytest.mark.register
def test_register_empty_fields_disabled_submit(browser, base_url):
    # Кнопка активна всегда, валидация после нажатия.
    browser.get(base_url+REGISTER_URL)

    wait_for_clickable(browser, SUBMIT_BUTTON_LOCATOR).click()

    element = browser.find_element(*USERNAME_LOCATOR)
    error_message = browser.execute_script("return arguments[0].validationMessage;", element)

    assert "Please fill out this field" in error_message

@pytest.mark.register
def test_register_invalid_email(browser, base_url):
    browser.get(base_url+REGISTER_URL)

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"not-email"
    password = "Password123"
    confirm = "Password123"
    age = "20"

    fill_register_form(browser, username, email, password, confirm, age)

    wait_for_clickable(browser, SUBMIT_BUTTON_LOCATOR).click()

    assert wait_for_element(browser, REGISTER_MESSAGE_LOCATOR).is_displayed()

@pytest.mark.register
def test_register_password_mismatch(browser, base_url):
    browser.get(base_url+REGISTER_URL)

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Password123"
    confirm = "WrongPassword1"
    age = "20"

    fill_register_form(browser, username, email, password, confirm, age)

    wait_for_clickable(browser, SUBMIT_BUTTON_LOCATOR).click()

    error_message = wait_for_element(browser, REGISTER_MESSAGE_LOCATOR).text
    assert "Пароли не совпадают" in error_message

@pytest.mark.register
def test_register_short_password(browser, base_url):
    browser.get(base_url+REGISTER_URL)

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Ab1!"
    confirm = "Ab1!"
    age = "20"

    fill_register_form(browser, username, email, password, confirm, age)

    wait_for_clickable(browser, SUBMIT_BUTTON_LOCATOR).click()

    error_message = wait_for_element(browser, REGISTER_MESSAGE_LOCATOR).text
    assert "Пароль не соответствует требованиям" in error_message
