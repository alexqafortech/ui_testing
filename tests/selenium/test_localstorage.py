import pytest

@pytest.mark.javascript
def test_cart_stored_in_localstorage(catalog_page, cart_page):
    catalog_page.open()

    catalog_page.get_products()

    start_storage_count = cart_page.get_localstorage_cart_count()
    start_cart_count = cart_page.header.get_cart_count()

    catalog_page.add_first_product_to_cart()
    catalog_page.alert_accept()

    cart_page.wait_until(
        lambda _: cart_page.header.get_cart_count() == start_cart_count + 1
    )

    final_cart_count = cart_page.header.get_cart_count()
    final_storage_count = cart_page.get_localstorage_cart_count()

    assert final_cart_count == start_cart_count + 1
    assert final_storage_count == start_storage_count + 1

@pytest.mark.javascript
def test_clear_localstorage_empties_cart(catalog_page, cart_page):
    catalog_page.open()

    catalog_page.get_products()

    start_cart_count = cart_page.header.get_cart_count()

    catalog_page.add_first_product_to_cart()
    catalog_page.alert_accept()
    cart_page.wait_for_cart_count(start_cart_count + 1)

    assert cart_page.header.get_cart_count() == start_cart_count + 1

    cart_page.clear_localstorage_cart()
    catalog_page.refresh()

    catalog_page.get_products()
    cart_page.wait_for_cart_count(0)

    assert cart_page.header.get_cart_count() == 0
