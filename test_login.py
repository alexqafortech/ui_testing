import pytest
from selenium.webdriver.common.by import By
import time

LOGIN_URL = "/login"

@pytest.mark.auth
def test_login_form_gas_required_field(browser, base_url):
    browser.get(base_url + LOGIN_URL)
    login_area = browser.find_element(By.CSS_SELECTOR, '[name="email"]')
    assert login_area.is_displayed() == True
    password_area = browser.find_element(By.CSS_SELECTOR, '[type="password"]')
    assert password_area.is_displayed() == True
    submit_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    assert submit_button.is_displayed() == True

@pytest.mark.auth
def test_login_with_valid_credentials(browser, base_url):
    browser.get(base_url + LOGIN_URL)

    login_area = browser.find_element(By.CSS_SELECTOR, '[name="email"]')
    assert login_area.is_displayed() == True
    login_area.send_keys("test_user@shopmarket.ru")

    password_area = browser.find_element(By.CSS_SELECTOR, '[type="password"]')
    assert password_area.is_displayed() == True
    password_area.send_keys("Password123")

    submit_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    assert submit_button.is_displayed() == True
    submit_button.click()
    time.sleep(2) # TODO: заменить на explicit wait в практике 3

    assert "/login" not in browser.current_url

@pytest.mark.auth
def test_login_with_invalid_password_shows_error(browser, base_url):
    browser.get(base_url + LOGIN_URL)

    login_area = browser.find_element(By.CSS_SELECTOR, '[name="email"]')
    assert login_area.is_displayed() == True
    login_area.send_keys("test_user@shopmarket.ru")


    password_area = browser.find_element(By.CSS_SELECTOR, '[type="password"]')
    assert password_area.is_displayed() == True
    password_area.send_keys("WrongPassword")

    submit_button = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    assert submit_button.is_displayed() == True
    submit_button.click()
    time.sleep(2) # TODO: заменить на explicit wait в практике 3

    error_message = browser.find_element(By.CSS_SELECTOR, '.error-message-container')
    assert error_message.is_displayed() == True

@pytest.mark.auth
@pytest.mark.parametrize(
    "strategy, value",
    [
        pytest.param(By.NAME, "email", id="by_name"), # Самый приоритетный, имя элемента вряд ли будет меняться
        pytest.param(By.CSS_SELECTOR, "input[name='email']", id="by_css_attr"), # Второй по приоритету, буквально то же самое, что и первый вариант, только длиннее
        pytest.param(By.CSS_SELECTOR, "form div:first-child input", id="by_css_position"), # Четвертый/Пятый по приоритету, сломается при первом же редизайне
        pytest.param(By.XPATH, "//input[@name='email']", id = "by_xpath_attr"), # Третий по приоритету, то же самое что и первый вариант и второй вариант, только через XPATH
        pytest.param(By.XPATH, "//label[normalize-space()='Email']/following-sibling::input", id = "by_xpath_text"), # Четвертый/Пятый по приоритету, так же сломается при редизайне, или изменении значения label
    ]
)
def test_email_field_findable_by_different_strategies(browser, base_url, strategy, value):
    browser.get(base_url + LOGIN_URL)
    time.sleep(1)
    email_element = browser.find_element(strategy, value)
    time.sleep(1)
    assert email_element.is_displayed() == True
    assert email_element.tag_name == "input"


