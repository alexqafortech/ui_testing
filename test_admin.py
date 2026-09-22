import pytest
import time
from selenium.webdriver.common.by import By

ADMIN_URL = "/admin"

@pytest.mark.admin
def test_admin_table_shows_users(browser, base_url):
    browser.get(base_url + ADMIN_URL)
    time.sleep(2)
    items = browser.find_elements(By.CSS_SELECTOR, "#users-table > div > table > tbody > tr")
    assert len(items) > 5

@pytest.mark.admin
def test_find_user_row_by_login (browser, base_url):
    browser.get(base_url + ADMIN_URL)
    time.sleep(2)
    item = browser.find_element(By.XPATH, "//td[contains(., 'test_user')]/following-sibling::td[1]")
    assert item.text == "test_user@shopmarket.ru"

@pytest.mark.admin
def test_block_active_user(browser, base_url):
    browser.get(base_url + ADMIN_URL)
    time.sleep(2)
    item = browser.find_element(By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[5]"
                                          "/div/button[contains(text(), 'Заблокировать')]")
    item.click()
    time.sleep(2)
    alert = browser.switch_to.alert
    alert.accept()
    time.sleep(2)

    new_item = browser.find_element(By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[3]")
    assert new_item.text == "Заблокирован"
