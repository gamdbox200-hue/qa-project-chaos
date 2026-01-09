from playwright.sync_api import Page, expect

class UsersPage:
    def __init__(self, page: Page):
        self.page = page
        # Локаторы (храним их в одном месте)
        self.user_rows = page.locator("tr")
        self.search_input = page.get_by_placeholder("Search...") # пример на будущее

    def navigate(self):
        self.page.goto("https://jsonplaceholder.typicode.com/users", wait_until="domcontentloaded")

    def verify_user_exists(self, name: str):
        # Проверяем, что текст виден на странице
        expect(self.page.get_by_text(name)).to_be_visible()