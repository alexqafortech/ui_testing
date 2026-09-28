import pytest
import uuid
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from pages.orders_page import OrdersPage

def test_full_purchase_flow(login_page, catalog_page, cart_page, orders_page, reset_db):
    # Вход в аккаунт
    login_page.open()
    login_page.login("test_user@shopmarket.ru", "Password123")

    # Открытие каталога + добавление товара + проверка счетчика корзины
    catalog_page.open()
    catalog_page.add_product_to_cart(1)
    cart_count = catalog_page.header.get_cart_count()
    assert cart_count == 1

    # Открытие корзины + проверка, что товар присутствует + запоминание суммы
    cart_page.open()
    cart_items = cart_page.get_items_count()
    assert cart_items >= 1
    start_summ = cart_page.get_total()

    # Применение промокода + проверка появления скидки + проверка, что сумма поменялась + оформление заказа
    cart_page.apply_promo("SAVE20")
    assert cart_page.get_discount()
    final_summ = cart_page.get_total()
    assert start_summ != final_summ
    orders_page = cart_page.checkout()
    orders_page.open()
    assert orders_page.get_order_count() >= 1



