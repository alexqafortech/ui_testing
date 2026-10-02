import pytest
from playwright.sync_api import expect

from pages.playwright.login_page import PlaywrightLoginPage
from pages.playwright.catalog_page import PlaywrightCatalogPage
from pages.playwright.cart_page import PlaywrightCartPage
from pages.playwright.orders_page import PlaywrightOrdersPage


@pytest.mark.e2e
def test_full_purchase_flow_parallel_1(parallel_page, parallel_user_registered):
    user = parallel_user_registered

    login = PlaywrightLoginPage(parallel_page)
    login.open()
    login.login(
        user["email"],
        user["password"]
    )

    username_element = login.get_username()

    expect(username_element).to_have_text(
        user["username"]
    )

    catalog = PlaywrightCatalogPage(parallel_page)
    catalog.open()

    catalog.add_product_by_name("iPhone 15")

    expect(
        catalog.header.get_cart_count()
    ).to_have_text("1")

    cart = PlaywrightCartPage(parallel_page)
    cart.open()

    expect(cart.cart_item).to_have_count(1)

    cart.apply_promo("SAVE20")

    expect(
        cart.get_discount()
    ).to_be_visible()

    cart.checkout()

    orders = PlaywrightOrdersPage(parallel_page)
    orders.open()

    expect(
        orders.get_orders()
    ).not_to_have_count(0)

@pytest.mark.e2e
def test_full_purchase_flow_parallel_2(parallel_page, parallel_user_registered):
    user = parallel_user_registered

    login = PlaywrightLoginPage(parallel_page)
    login.open()
    login.login(
        user["email"],
        user["password"]
    )

    username_element = login.get_username()

    expect(username_element).to_have_text(
        user["username"]
    )

    catalog = PlaywrightCatalogPage(parallel_page)
    catalog.open()

    catalog.add_product_by_name("iPhone 15")

    expect(
        catalog.header.get_cart_count()
    ).to_have_text("1")

    cart = PlaywrightCartPage(parallel_page)
    cart.open()

    expect(cart.cart_item).to_have_count(1)

    cart.apply_promo("SAVE20")

    expect(
        cart.get_discount()
    ).to_be_visible()

    cart.checkout()

    orders = PlaywrightOrdersPage(parallel_page)
    orders.open()

    expect(
        orders.get_orders()
    ).not_to_have_count(0)

@pytest.mark.e2e
def test_full_purchase_flow_parallel_3(parallel_page, parallel_user_registered):
    user = parallel_user_registered

    login = PlaywrightLoginPage(parallel_page)
    login.open()
    login.login(
        user["email"],
        user["password"]
    )

    username_element = login.get_username()

    expect(username_element).to_have_text(
        user["username"]
    )

    catalog = PlaywrightCatalogPage(parallel_page)
    catalog.open()

    catalog.add_product_by_name("iPhone 15")

    expect(
        catalog.header.get_cart_count()
    ).to_have_text("1")

    cart = PlaywrightCartPage(parallel_page)
    cart.open()

    expect(cart.cart_item).to_have_count(1)

    cart.apply_promo("SAVE20")

    expect(
        cart.get_discount()
    ).to_be_visible()

    cart.checkout()

    orders = PlaywrightOrdersPage(parallel_page)
    orders.open()

    expect(
        orders.get_orders()
    ).not_to_have_count(0)

@pytest.mark.e2e
def test_full_purchase_flow_parallel_4(parallel_page, parallel_user_registered):
    user = parallel_user_registered

    login = PlaywrightLoginPage(parallel_page)
    login.open()
    login.login(
        user["email"],
        user["password"]
    )

    username_element = login.get_username()

    expect(username_element).to_have_text(
        user["username"]
    )

    catalog = PlaywrightCatalogPage(parallel_page)
    catalog.open()

    catalog.add_product_by_name("iPhone 15")

    expect(
        catalog.header.get_cart_count()
    ).to_have_text("1")

    cart = PlaywrightCartPage(parallel_page)
    cart.open()

    expect(cart.cart_item).to_have_count(1)

    cart.apply_promo("SAVE20")

    expect(
        cart.get_discount()
    ).to_be_visible()

    cart.checkout()

    orders = PlaywrightOrdersPage(parallel_page)
    orders.open()

    expect(
        orders.get_orders()
    ).not_to_have_count(0)