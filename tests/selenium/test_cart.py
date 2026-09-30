import pytest
import time

@pytest.mark.cart
def test_add_to_cart_increases_counter_lambda(catalog_page):
    start = time.time()
    catalog_page.open()

    catalog_page.get_products()
    start_cart_value = catalog_page.header.get_cart_count()

    for index in range(3):
        expected_value = start_cart_value + index + 1

        catalog_page.add_product_to_cart_and_wait(
            index,
            expected_value
        )

    final_value = catalog_page.header.get_cart_count()

    assert final_value == start_cart_value + 3, (
        f"Ожидали в корзине {start_cart_value + 3}, "
        f"но получили {final_value}"
    )

    duration = time.time() - start
    print(f"Тест занял {duration:.2f}s")

@pytest.mark.cart
def test_add_three_products_to_cart(catalog_page):
    start = time.time()
    catalog_page.open()

    catalog_page.get_products()
    start_cart_value = catalog_page.header.get_cart_count()

    for index in range(3):
        expected_value = start_cart_value + index + 1

        catalog_page.add_product_to_cart(index)
        catalog_page.wait_for_cart_count(expected_value)

    final_value = catalog_page.header.get_cart_count()

    assert final_value == start_cart_value + 3, (
        f"Ожидали в корзине {start_cart_value + 3}, "
        f"но получили {final_value}"
    )
    duration = time.time() - start
    print(f"Тест занял {duration: .2f}s")

@pytest.mark.cart
def test_cart_page_shows_added_products(catalog_page, cart_page):
    start = time.time()
    catalog_page.open()

    catalog_page.get_products()

    start_cart_value = catalog_page.header.get_cart_count()

    catalog_page.add_first_product_to_cart()
    catalog_page.alert_accept()
    catalog_page.wait_for_cart_count(start_cart_value + 1)

    cart_page.open()

    cart_products = cart_page.get_items_count()

    assert cart_products == 1
    duration = time.time() - start
    print(f"Тест занял {duration: .2f}s")
