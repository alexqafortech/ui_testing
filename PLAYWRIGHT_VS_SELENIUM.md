1.2. Selenium (количество строк кода - 4 (не считая маркер, название теста):
```Selenium
@pytest.mark.main_page
def test_main_page_has_hero_heading(main_page):
    main_page.open()
    heading = main_page.find(main_page.HERO_TITLE)
    assert heading.is_displayed()
    assert heading.text.strip() != ""
```
1.1. Playwright (количество строк кода - 2 (не считая маркер, название теста)):
```Playwright
@pytest.mark.smoke
def test_main_page_hero_banner(page):
    page.goto("/")
    assert page.inner_text("h1") != ""
```

2. При переходе на Playwright исчезли дополнительные ожидания рендеринга страницы, так же стало меньше import, код стал чище и короче
3. В Selenium для того, чтобы менять режим headed и headless была необходима отдельная фикстура, в Playwright этой необходимости нет, можно сразу всё запускать через терминал
4. Selenium (5 smoke тестов) - 10.76s. Playwright (7 smoke-тестов) - 8.78s

5. Вывод:
По моему субъективному мнению, на первый взгляд, не углубляясь, Playwright, кажется более рентабельным вариантом для автоматизации тестирования, но если уже есть тестовая база на Selenium, то нет смысла всё переписывать на Playwright, потому что разница в скорости не такая и большая. Огромным плюсом Playwright я считаю, что он уже содержит в себе авто-ожидания, и нет необходимости прописывать отдельные фикстуры для этого. 