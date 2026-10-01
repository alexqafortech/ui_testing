import pytest
from conftest import catalog_page_auth
from tests.selenium.test_data import INVALID_REGISTRATION, PROMO_CODES

@pytest.mark.register
@pytest.mark.parametrize("username, email, password, confirm, age, expected_error", INVALID_REGISTRATION,
                         ids = ["Different_password", "Short_password", "No_digits_username", "Short_username"])
def test_register_validation(register_page, username, email, password, confirm, age, expected_error):
    register_page.open()

    register_page.register(username, email, password, age, confirm)

    error_message = register_page.get_error_message()

    assert expected_error in error_message

@pytest.mark.cart
@pytest.mark.parametrize("code, should_discount", PROMO_CODES)
def test_promo_codes(code, should_discount, catalog_page_auth, catalog_page, cart_page, reset_db):
    catalog_page.open()
    catalog_page.add_product_to_cart(1)

    cart_count = catalog_page.header.get_cart_count()

    assert cart_count == 1

    cart_page.open()
    cart_page.apply_promo(code)
    result = cart_page.is_visible_discount()
    assert result == should_discount

