Codegen output
```
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://82.146.39.180:3000/")
    page.get_by_role("link", name="Каталог").click()
    page.once("dialog", lambda dialog: dialog.dismiss())
    page.get_by_role("button", name="В корзину").first.click()
    page.get_by_role("link", name="1", exact=True).click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

```

Тест написанный вручную:
```
@pytest.mark.catalog
def test_add_to_cart_via_po(catalog_page):
    catalog_page.open()
    catalog_page.add_product_by_name("iPhone 15")
    expect(catalog_page.header.get_cart_count()).to_have_text("1")
```

В целом полученный код через Codegen на этом примере вышел не так уж и плох, но код написанный вручную получается более
лаконичным и понятным человеку, в связи с понятными названиями функций, а так же засчет Page Object, вся работа происходит
"под капотом", и тестировщику остается только добавить проверки. Также код полученный через Codegen не содержит в себе
проверок, он просто выполняет действия, при этом ничего не проверяя. Ещё одной проблемой является хардкод локатора, который
используется для перехода в корзину ```page.get_by_role("link", name="1", exact=True).click()```, локатор упадет в случае,
если товаров окажется несколько.

Ручной trace:
trace содержит 21 шаг:
1) Create page
2) Navigate "/login"
3) Fill email input
4) Fill password input
5) Click button "Войти"
6) Expect "to_have_text" "Имя пользователя"
7) Navigate "/catalog"
8) Click button "В корзину"
9) Expect "to_have_text" "Количество товаров в корзине в header"
10) Navigate "/cart"
11) Expect "to_have_count" "Количество товаров в корзине"
12) Fill promo input
13) Click button "Применить"
14) Expect "to_be_visible" "Отображение скидки"
15) Click button "Оформить заказ"
16) Accept dialog "Имя получателя"
17) Accept dialog "Телефон"
18) Accept dialog "Адрес"
19) Wait_for_event "frame.wait_for_load_state"
20) Navigate "/orders"
21) Expect "not_to_have_count"

На шаге "Добавить в корзину" снапшот показывает, что курсор наведён на кнопку "В корзину"

Видны следующие запросы:
1) Шаг "Navigate '/login'"
   1) login GET 200
   2) cdn.tailwindcss.com GET 302
   3) style.css GET 200
   4) api.js GET 200
   5) auth.js GET 200
   6) cart-store.js GET 200
   7) header.js GET 200
   8) 3.4.17 GET 200
   9) me GET 401
2) Шаг "Click button 'Войти'"
    1) login POST 200
3) Шаг "Expect 'to_have_text' 'Имя пользователя'"
   1) 82.146.39.180:300 GET 200
   2) cdn.tailwindcss.com GET 200
   3) style.css GET 304
   4) api.js GET 304
   5) cart-store.js GET 304
   6) header.js GET 304
   7) me GET 200
   8) products GET 200
   9) cart GET 200
   10) Четыре запроса GET для картинок продуктов
4) Шаг "Navigate '/catalog'"
   1) catalog GET 200
   2) cdn.tailwindcss.com GET 200
   3) style.css GET 304
   4) api.js GET 304
   5) auth.js GET 304
   6) cart-store.js GET 304
   7) header.js GET 304
   8) me GET 200
   9) me GET 200
5) Шаг "Click button 'В корзину'"
   1) cart GET 200
   2) products GET 200
   3) wishlist GET 200
   4) Пять запросов GET для картинок продуктов
   5) cart POST 200
6) Шаг "Expect "to_have_text" 'Количество товаров в корзине в header'"
   1) cart GET 200
7) Шаг "Navigate '/cart'"
   1) cart GET 200
   2) cdn.tailwindcss.com GET 200
   3) style.css GET 304
   4) api.js GET 304
   5) auth.js GET 304
   6) cart-store.js GET 304
   7) header.js GET 304
   8) me GET 200
   9) me GET 200
8) Шаг "Fill promo input"
   1) cart GET 200
   2) cart GET 200
   3) iphone-15-pro.svg GET 304
9) Шаг "Click button 'Применить'"
   1) promo POST 200
10) Шаг "Click button 'Оформить заказ'"
    1) orders POST 201
11) Шаг "Wait_for_event 'frame.wait_for_load_state'"
    1) 10043 GET 200
    2) cdn.tailwindcss.com GET 200
    3) style.css GET 304
    4) api.js GET 304
    5) auth.js GET 304
    6) cart-store.js GET 304
    7) header.js GET 304
    8) me GET 200
    9) 10043 GET 200
    10) cart GET 200
12) Шаг "Navigate '/orders'"
    1) orders GET 200
    2) cdn.tailwindcss.com GET 200
    3) style.css GET 304
    4) api.js GET 304
    5) auth.js GET 304
    6) cart-store.js GET 304
    7) header.js GET 304
    8) me GET 200
    9) me GET 200
13) Шаг "Expect 'not_to_have_count'"
    1) cart GET 200
    2) orders GET 200

Самым долгим шагом оказался шаг "Expect 'to_have_text' 'Имя пользователя'" - 1.3s

При поломке, в Trace отображается на каком шаге упал тест(поменял ожидаемый результат с "Иванов Дмитрий" на 
"Иванов Дмитрий1"), так же видная причина, по которой тест упал "Expect failed"
