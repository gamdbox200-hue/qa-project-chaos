import pytest
from typing import Generator
from playwright.sync_api import Playwright, APIRequestContext


def test_get_user_and_check_email(api_request_context):
    # Отправляем GET запрос на сервер
    response = api_request_context.get("/users/1")
    
    # Проверяем статус код (200 OK)
    assert response.ok
    
    # Парсим JSON ответ
    user_data = response.json()
    print(f"\nДанные юзера: {user_data['name']} - {user_data['email']}")
    
    # Проверка данных
    assert user_data["username"] == "Bret"
    assert "@" in user_data["email"]

def test_create_and_delete_post(api_request_context):
    # 1. CREATE (POST)
    new_post = {
        "title": "BlackBerry Movie Review",
        "body": "Great movie about tech history!",
        "userId": 1
    }
    create_resp = api_request_context.post("/posts", data=new_post)
    assert create_resp.status    == 201
    
    post_id = create_resp.json()["id"]
    print(f"\n🚀 Создан пост с ID: {post_id}")

    # 2. DELETE
    # Мы используем ID, который получили только что
    delete_resp = api_request_context.delete(f"/posts/{post_id}")
    
    # Статус 200 или 204 обычно означает успешное удаление
    assert delete_resp.ok
    print(f"🗑️ Пост {post_id} успешно удален")