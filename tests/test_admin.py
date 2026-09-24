import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from helpers.waits import wait_for_element, wait_for_clickable
from selenium.webdriver.support import expected_conditions as EC
import time

ADMIN_URL = "/admin"

@pytest.mark.admin
def test_admin_table_shows_users(browser, base_url):
    browser.get(base_url + ADMIN_URL)
    wait_for_element(browser, (By.CSS_SELECTOR, "#users-table > div > table > tbody > tr"))
    items = browser.find_elements(By.CSS_SELECTOR, "#users-table > div > table > tbody > tr")
    assert len(items) > 5

@pytest.mark.admin
def test_find_user_row_by_login (browser, base_url):
    browser.get(base_url + ADMIN_URL)
    item = (wait_for_element(browser, (By.XPATH, "//td[contains(., 'test_user')]/following-sibling::td[1]")).
            find_element(By.XPATH, "//td[contains(., 'test_user')]/following-sibling::td[1]"))
    assert item.text == "test_user@shopmarket.ru"

@pytest.mark.admin
def test_block_active_user(browser, base_url, refresh_data_base):
    browser.get(base_url + ADMIN_URL)
    wait_for_clickable(browser,(By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[5]/div/button[contains(text(), 'Заблокировать')]")).click()

    alert = browser.switch_to.alert
    alert.accept()

    wait = WebDriverWait(browser, 10)
    wait.until(EC.text_to_be_present_in_element((By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[3]"), "Заблокирован"))
    new_item = browser.find_element(By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[3]")
    assert new_item.text == "Заблокирован"
