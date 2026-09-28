import pytest

@pytest.mark.smoke
@pytest.mark.main_page
def test_main_page_has_correct_title(main_page):
    """Главная страница BuggyShop загружается с корректным заголовком."""
    main_page.open()
    assert "ШопМаркет" in main_page.get_hero_title()

@pytest.mark.main_page
def test_main_page_has_hero_heading(main_page):
    """На главной странице отображается заголовок hero-баннера."""
    main_page.open()
    heading = main_page.find(main_page.HERO_TITLE)
    assert heading.is_displayed()
    assert heading.text.strip() != ""

@pytest.mark.main_page
def test_cta_button_leads_to_catalog(main_page):
    """Клик по ссылке 'Каталог' в шапке ведёт на страницу каталога."""
    main_page.open()
    main_page.click_cta()
    main_page.wait_for_url_contains("/catalog")

@pytest.mark.parametrize("url_text, expected_url", [
    pytest.param("Каталог", "/catalog", id = "catalog_link"),
    pytest.param("Войти", "/login", id = "login_link"),
    pytest.param("Зарегистрироваться", "/register", id = "register_link"),
    pytest.param("ШопМаркет", "/", id = "main_link"),
    pytest.param("Поддержка", "/support", id = "support_link")
])
def test_header_link_leads_to_correct_page(main_page, url_text, expected_url):
    main_page.open()
    main_page.click((main_page.PARTIAL, url_text))
    main_page.wait_for_url_contains(expected_url)