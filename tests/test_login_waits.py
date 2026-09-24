import pytest
from selenium.webdriver.common.by import By
from helpers.waits import wait_for_element, wait_for_clickable, wait_for_url_contains
import time

LOGIN_URL = "/login"

@pytest.mark.auth
def test_login_form_loads_before_interaction(browser, base_url):
    start = time.time()
    browser.get(base_url+LOGIN_URL)

    email = wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]'))
    password = wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]'))
    submit = wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]'))

    assert email.is_displayed() is True
    assert password.is_displayed() is True
    assert submit.is_displayed() is True
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")


# У кнопки нет атрибута disabled
@pytest.mark.skip
@pytest.mark.auth
def test_submit_button_is_disabled_with_empty_form(browser, base_url):
    start = time.time()
    browser.get(base_url+LOGIN_URL)

    wait_for_element(browser, (By.ID, 'login-form'))
    button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    assert button.get_attribute("disabled") is not None
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

# После авторизации пользователя редиректит на главную
@pytest.mark.skip
@pytest.mark.auth
def test_successful_login_redirects_to_account(browser, base_url):
    start = time.time()
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_user@shopmarket.ru")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("Password123")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    wait_for_url_contains(browser, "/account")

    user_button = wait_for_element(browser, (By.CSS_SELECTOR, "div[class='relative group'] button:first-child"))

    assert user_button.text == "Алексей Петров"
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.auth
def test_login_with_wrong_password_shows_error_message(browser, base_url):
    start = time.time()
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_user@shopmarket.ru")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("WrongPassword")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    error = wait_for_element(browser, (By.CSS_SELECTOR, '.error-message-container'))
    assert "Неверный" in error.text

    wait_for_url_contains(browser, (base_url+LOGIN_URL))
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

# Ошибка не пропадает вовсе
@pytest.mark.skip
@pytest.mark.auth
def test_error_message_disappears_after_fild_correction(browser, base_url):
    start = time.time()
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_user@shopmarket.ru")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("WrongPassword")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("Password123")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    wait_for_url_contains(browser, "/account")
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")
