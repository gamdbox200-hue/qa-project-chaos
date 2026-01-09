from faker import Faker

fake = Faker()

def test_get_posts_with_client(api_client):
    # Используем фикстуру api_client
    response = api_client.get("/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_create_post_with_random_data(api_client, fake): # Используем нашу новую фикстуру
    payload = {
        "title": fake.sentence(),
        "body": fake.text(),
        "userId": fake.random_int(min=1, max=10)
    }
    response = api_client.post("/posts", json=payload)
    assert response.status_code == 201
   
def test_get_non_existent_post(api_client):
    # Запрашиваем заведомо несуществующий ID
    response = api_client.get("/posts/9999")
    
    # Проверяем, что сервер вернул 404 (а не 200 или 500)
    assert response.status_code == 404