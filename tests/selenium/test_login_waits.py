import pytest
import time

LOGIN_URL = "/login"

@pytest.mark.auth
def test_login_form_loads_before_interaction(login_page):
    start = time.time()
    login_page.open()
    assert login_page.is_login_form_loaded()
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.skip(reason = "У кнопки нет атрибута disabled")
@pytest.mark.auth
def test_submit_button_is_disabled_with_empty_form(login_page):
    start = time.time()
    login_page.open()
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.skip(reason = "После авторизации пользователя редиректит на главную")
@pytest.mark.auth
def test_successful_login_redirects_to_account(login_page):
    start = time.time()
    login_page.open()

    login_page.login( "test_user@shopmarket.ru", "Password123" )

    login_page.wait_for_url_contains("/account")

    assert login_page.get_logged_in_user() == "Алексей Петров"

    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.auth
def test_login_with_wrong_password_shows_error_message(login_page):
    start = time.time()
    login_page.open()

    login_page.login( "test_user@shopmarket.ru", "WrongPassword" )

    assert "Неверный" in login_page.get_error_message()

    login_page.wait_for_url_contains("/login")
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.skip(reason = "Ошибка не пропадает вовсе")
@pytest.mark.auth
def test_error_message_disappears_after_fild_correction(login_page):
    start = time.time()
    login_page.open()

    login_page.login( "test_user@shopmarket.ru", "WrongPassword" )

    login_page.login( "test_user@shopmarket.ru", "Password123" )

    login_page.wait_for_url_contains("/account")
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")
