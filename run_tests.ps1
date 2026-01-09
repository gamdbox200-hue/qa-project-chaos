docker run --rm -v ${PWD}:/app -e PYTHONPATH=/app -w /app qa-project-chaos pytest tests/test_api_db.py --alluredir=allure-results --clean-alluredir
allure serve allure-results