# 1. Импорты (обязательно)
from playwright.sync_api import sync_playwright, expect  # sync для простоты, async потом
import pytest

# 2. Фикстура для браузера (лучше в conftest.py, но пока здесь)
@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # visible для дебага
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

# 3. Сам тест
def test_successful_login(page):
    # Шаг 1: Открываем сайт (пример — публичный demo)
    page.goto("https://the-internet.herokuapp.com/login")

    # Шаг 2: Находим поле username по label
    username_field = page.get_by_label("Username")
    username_field.fill("tomsmith")  # fill = ввод текста

    # Шаг 3: Пароль по placeholder
    password_field = page.get_by_placeholder("Password")
    password_field.fill("SuperSecretPassword!")

    # Шаг 4: Кнопка Login по роли и тексту
    login_button = page.get_by_role("button", name="Login")
    login_button.click()

    # Шаг 5: Проверяем успех (по тексту)
    success_message = page.get_by_text("You logged into a secure area!")
    expect(success_message).to_be_visible()  # assert-like, ждёт автоматически

    # Бонус: скриншот на успех
    page.screenshot(path="success_login.png")