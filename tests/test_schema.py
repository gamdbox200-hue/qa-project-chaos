import allure
from jsonschema import validate
from tests.schemas import POST_SCHEMA

def test_get_post_schema_optimized(posts_api):
    response = posts_api.get_post(1)
    
    with allure.step("Валидация JSON-схемы"):
        validate(instance=response.json(), schema=POST_SCHEMA)