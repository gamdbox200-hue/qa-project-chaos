from pages.base_page import BasePage
import allure

class ExamplePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Описываем локаторы (элементы)
        self.header = page.locator("h1")

    def get_header_text(self):
        with allure.step("Получение текста заголовка"):
            return self.header.text_content()