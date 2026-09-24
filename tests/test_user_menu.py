import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from helpers.waits import wait_for_element, wait_for_clickable, wait_for_url_contains

TEST_USER = ("test_user@shopmarket.ru", "Password123")
LOGIN_URL = "/login"
USER_MENU = (By.CSS_SELECTOR, "div[class='relative group'] div")

@pytest.mark.navigation
def test_user_menu_navigate_to_profile(browser, base_url, create_user_with_hard_password, refresh_data_base):
    browser.get(base_url + LOGIN_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, '[name="email"]')).send_keys("test_hard_pass@test.com")
    wait_for_element(browser, (By.CSS_SELECTOR, '[type="password"]')).send_keys("HardPassword123!")
    wait_for_clickable(browser, (By.CSS_SELECTOR, '[type="submit"]')).click()
    WebDriverWait(browser, 10).until(
        lambda d: str(browser.current_url) == base_url + "/")

    user_menu = wait_for_element(browser, (By.CSS_SELECTOR, "div[class='relative group']"))
    ActionChains(browser).move_to_element(user_menu).perform()
    wait_for_clickable(browser, (By.CSS_SELECTOR, "a[href='/profile']")).click()

    wait_for_url_contains(browser, "/profile")
    assert wait_for_element(browser, (By.ID, "profile-content"))
