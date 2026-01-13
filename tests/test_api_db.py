import pytest
import allure

@allure.feature("Database Integration")
@allure.story("CRUD operations with Posts")
@pytest.mark.parametrize("title, body, test_case_name", [
    ("12345", "Body", "Нижняя граница: 5 символов"),             # Boundary (Min)
    ("A" * 52, "Body", "Класс эквивалентности: среднее значение"), # Equivalence Class
    ("A" * 100, "Body", "Верхняя граница: 100 символов"),        # Boundary (Max)
    ("!@#$%", "Body", "Спецсимволы (позитивный)"),                # Special chars
    ("Кириллица", "Тело", "Проверка кодировки (UTF-8)")           # Encoding
])
def test_db_title_boundaries(db_session, title, body, test_case_name):
    # Обновляем динамическое название теста в Allure
    allure.dynamic.title(f"Проверка заголовка: {test_case_name}")
    
    with allure.step(f"Создание записи в БД: {test_case_name}"):
        db_session.create_post(title, body, 1)
        
    with allure.step("Поиск записи по точному заголовку"):
        post = db_session.get_post_by_title(title)
        
    with allure.step("Проверка корректности данных"):
        assert post is not None, f"Запись с заголовком '{test_case_name}' не найдена в БД"
        assert post[1] == title
        allure.attach(f"Заголовок: {title}\nДлина: {len(title)}", 
                      name="Детали проверки", 
                      attachment_type=allure.attachment_type.TEXT)
        
    with allure.step("Очистка данных"):
        db_session.delete_post_by_title(title)