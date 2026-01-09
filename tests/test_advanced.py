import allure
from jsonschema import validate

def test_db_with_faker(db_session, fake):
    # Генерируем случайные данные
    random_title = fake.sentence(nb_words=3)
    random_body = fake.text()
    
    with allure.step(f"Создание записи с рандомным заголовком: {random_title}"):
        db_session.create_post(random_title, random_body, 1)
    
    with allure.step("Проверка записи в БД"):
        post = db_session.get_post_by_title(random_title)
        assert post is not None
        assert post[1] == random_title
    
    # Очистка
    db_session.delete_post_by_title(random_title)

# Описываем, как ДОЛЖЕН выглядеть пост
POST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "title": {"type": "string"},
        "body": {"type": "string"},
        "userId": {"type": "number"}
    },
    "required": ["id", "title", "userId"] # Эти поля обязательpy
}

def test_api_schema_validation(base_url):
    import requests
    response = requests.get(f"{base_url}/posts/1")
    
    with allure.step("Валидация JSON-схемы ответа API"):
        validate(instance=response.json(), schema=POST_SCHEMA)
    
    assert response.status_code == 200