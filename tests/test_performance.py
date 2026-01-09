import pytest
import time

def test_api_performance(posts_api):
    start_time = time.time()
    response = posts_api.get_post(1)
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000 # Переводим в мс
    print(f"\nВремя ответа: {duration:.2f} мс")
    
    assert duration < 500, f"API тормозит! Ответ занял {duration} мс"