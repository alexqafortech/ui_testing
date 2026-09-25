import pytest
import uuid

@pytest.mark.register
def test_register_success(register_page):
    register_page.open()

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Password123"
    age = "20"

    register_page.register(username, email, password, age)

    #Чекбокс согласия не реализован

    message = register_page.get_success_message()
    assert "Регистрация успешна! Подтвердите email по ссылке" in message

@pytest.mark.register
def test_register_empty_fields_disabled_submit(register_page):
    # Кнопка активна всегда, валидация после нажатия.
    register_page.open()

    register_page.click(register_page.SUBMIT_BUTTON_LOCATOR)
    error_message = register_page.native()

    assert "Please fill out this field" in error_message

@pytest.mark.register
def test_register_invalid_email(register_page):
    register_page.open()

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"not-email"
    password = "Password123"
    age = "20"

    register_page.register(username, email, password, age)

    assert register_page.get_error_message()

@pytest.mark.register
def test_register_password_mismatch(register_page):
    register_page.open()

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Password123"
    confirm = "WrongPassword1"
    age = "20"

    register_page.register(username, email, password, age, confirm)

    error_message = register_page.get_error_message()
    assert "Пароли не совпадают" in error_message

@pytest.mark.register
def test_register_short_password(register_page):
    register_page.open()

    username = f"test{uuid.uuid4().hex[:8]}"
    email = f"test{uuid.uuid4().hex[:8]}@test.com"
    password = "Ab1!"
    age = "20"

    register_page.register(username, email, password, age)

    error_message = register_page.get_error_message()
    assert "Пароль не соответствует требованиям" in error_message
