import allure

@allure.feature("API Error Handling")
@allure.story("Get non-existing post")
def test_get_non_existing_post(posts_api):
    # Запрашиваем пост, которого нет (например, с ID 9999)
    response = posts_api.get_post(9999)
    
    with allure.step("Проверка, что API возвращает 404"):
        assert response.status_code == 404