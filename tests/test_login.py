import pytest
from selenium.webdriver.common.by import By
from helpers.waits import wait_for_element, wait_for_clickable
from selenium.webdriver.support.ui import WebDriverWait

LOGIN_URL = "/login"

@pytest.mark.auth
def test_login_form_gas_required_field(browser, base_url):
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]'))
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]'))
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="submit"]'))

@pytest.mark.auth
def test_login_with_valid_credentials(browser, base_url):
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_user@shopmarket.ru")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("Password123")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    WebDriverWait(browser, 10).until(lambda d: str(browser.current_url) == base_url+"/")
    user_button = wait_for_element(browser, (By.CSS_SELECTOR, "div[class='relative group'] button:first-child"))

    assert user_button.text == "Алексей Петров"

@pytest.mark.auth
def test_login_with_invalid_password_shows_error(browser, base_url):
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_user@shopmarket.ru")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("WrongPassword")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()

    wait_for_element(browser, (By.CSS_SELECTOR, '.error-message-container'))

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

    email_element = wait_for_element(browser, (strategy, value))

    assert email_element.is_displayed() == True
    assert email_element.tag_name == "input"
