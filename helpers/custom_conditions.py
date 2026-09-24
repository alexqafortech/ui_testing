from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def cart_count_equals(expected: int, locator: tuple):

    def condition(browser):
        try:
            counter_element = browser.find_element(*locator)
            text_value = counter_element.get_attribute("textContent").strip()
            current_count = int(text_value) if text_value else 0
            return current_count == expected
        except (NoSuchElementException, ValueError):
            return False
    return condition
