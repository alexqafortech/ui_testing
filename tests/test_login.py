import pytest
from selenium.webdriver.common.by import By

LOGIN_URL = "/login"

@pytest.mark.auth
def test_login_form_has_required_field(login_page):
    login_page.open()

    assert login_page.is_visible(login_page.EMAIL_INPUT) == True
    assert login_page.is_visible(login_page.PASSWORD_INPUT) == True
    assert login_page.is_visible(login_page.SUBMIT_BUTTON) == True

@pytest.mark.auth
def test_login_with_valid_credentials(login_page):
    login_page.open()

    login_page.login("test_user@shopmarket.ru", "Password123")
    name = login_page.get_logged_in_user()

    assert name == "Алексей Петров"

@pytest.mark.auth
def test_login_with_invalid_password_shows_error(login_page):
    login_page.open()

    login_page.login("test_user@shopmarket.ru", "WrongPassword")
    login_page.get_error_message()

    assert login_page.is_visible(login_page.ERROR_MESSAGE) == True

# Бонусное задание с разными вариантами поиска элемента, поэтому By остается
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
def test_email_field_findable_by_different_strategies(login_page, strategy, value):
    login_page.open()

    assert login_page.find((strategy, value))
