from pages.example_page import ExamplePage
import allure

@allure.feature("UI Automation")
@allure.story("Page Object Model implementation")
def test_pom_example(page):
    example_page = ExamplePage(page)
    
    example_page.navigate("https://example.com")
    header_text = example_page.get_header_text()
    
    with allure.step(f"Проверка заголовка: {header_text}"):
        assert header_text == "Example Domain"