import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url):
        with allure.step(f"Переход по адресу {url}"):
            self.page.goto(url)