import requests
import allure
import json
import logging


# Настройка логгера
logging.basicConfig(
    filename='api_tests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class PostsClient:
    def __init__(self, base_url):
        self.base_url = f"{base_url}/posts"

    def get_post(self, post_id):
        with allure.step(f"GET запрос на получение поста #{post_id}"):
            response = requests.get(f"{self.base_url}/{post_id}")
            
            # Добавляем аттачмент с телом ответа
            allure.attach(
                json.dumps(response.json(), indent=4), 
                name="Response Body", 
                attachment_type=allure.attachment_type.JSON
            )
            
            # Добавляем лог статус-кода
            allure.attach(
                str(response.status_code), 
                name="Status Code", 
                attachment_type=allure.attachment_type.TEXT
            )
            
            return response
        
    def get_post(self, post_id):
        logging.info(f"Отправка запроса к посту {post_id}")
        response = requests.get(f"{self.base_url}/{post_id}")
        logging.info(f"Получен ответ со статусом {response.status_code}")
        # ... allure.attach ...
        return response