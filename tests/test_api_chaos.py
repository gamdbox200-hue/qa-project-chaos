import json

def test_mock_form_submission(page, form_page, fake):
    # Перехватываем любой POST запрос на этом домене
    def handle_post(route):
        print(f"\n🔥 ПЕРЕХВАЧЕНО: {route.request.method} {route.request.url}")
        
        # Возвращаем "сломанный" ответ от сервера
        route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Chaos Monkey says NO", "status": "fail"})
        )

    # Устанавливаем роут только для POST запросов
    # Регулярка означает: любой URL, но только если метод POST
    page.route("**/*", lambda route: handle_post(route) if route.request.method == "POST" else route.continue_())

    page.goto("https://practice-automation.com/form-fields/")
    
    # Заполняем форму через твой Page Object
    form_page.fill_form(fake.name(), fake.email(), "Testing Mocking")
    
    # Нажимаем сабмит и смотрим в консоль пайтона
    form_page.submit()
    
    # Даем время увидеть результат или ошибку на странице
    page.wait_for_timeout(2000)