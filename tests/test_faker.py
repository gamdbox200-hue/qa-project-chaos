import pytest
import allure

@allure.feature("Data Generation")
@allure.story("Testing with Faker")
def test_post_creation_with_faker(db_session, fake):
    # Генерируем данные на лету
    title = fake.sentence(nb_words=5) # Случайное предложение из 5 слов
    body = fake.paragraph(nb_sentences=3) # Случайный абзац
    
    with allure.step(f"Создаем пост с рандомным заголовком: {title}"):
        db_session.create_post(title, body, 1)
        
    with allure.step("Проверяем наличие записи в БД"):
        post = db_session.get_post_by_title(title)
        assert post is not None
        assert post[1] == title
        
    with allure.step("Удаляем тестовые данные"):
        db_session.delete_post_by_title(title)