import pytest
from playwright.sync_api import Page, APIRequestContext

def test_api_to_ui_verification(api_request_context: APIRequestContext, page: Page):
    # 1. ШАГ API: Получаем данные пользователя с ID 2
    response = api_request_context.get("/users/2")
    assert response.ok
    user_name = response.json()["name"] # Это "Ervin Howell"
    print(f"\nAPI: Получено имя пользователя - {user_name}")

    # 2. ШАГ UI: Идем на страницу, где этот пользователь должен быть
    # Мы используем тот же jsonplaceholder, но их "живую" страницу постов
    page.goto("https://jsonplaceholder.typicode.com/", wait_until="domcontentloaded",timeout=60000)
    
    # Кликнем на ссылку 'Users' (эмулируем действия юзера)
    page.goto("https://jsonplaceholder.typicode.com/users", wait_until="domcontentloaded")
    
    # 3. ПРОВЕРКА: Проверяем, что имя из API есть на странице
    # Ждем появления текста
    assert page.get_by_text(user_name).is_visible()
    print(f"UI: Имя {user_name} успешно найдено!")