import pytest
import allure

@allure.feature("Database Integration")  # Группировка в отчете
@allure.story("CRUD operations with Posts") # Подгруппа
@pytest.mark.parametrize("title, body", [
    ("Short", "Body 1"),
    ("Very Looooooong Title Check", "Body 2"),
    ("!@#$%^&*()", "Special Characters Check")
])
def test_db_multiple_titles(db_session, title, body):
    with allure.step(f"Создание записи в БД с заголовком: {title}"):
        db_session.create_post(title, body, 1)
        
    with allure.step("Поиск созданной записи в базе данных"):
        post = db_session.get_post_by_title(title)
        
    with allure.step("Проверка корректности данных"):
        assert post is not None
        assert post[1] == title
        allure.attach(f"Заголовок: {title}\nТело: {body}", name="Данные теста", attachment_type=allure.attachment_type.TEXT)
        
    # Чистка (Teardown) тоже автоматически попадет в логи
    db_session.delete_post_by_title(title)