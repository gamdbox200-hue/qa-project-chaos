from playwright.sync_api import Page

class FormPage:
    def __init__(self, page: Page):
        self.page = page
        # Используем конкретные ID через метод locator
        # Это исключает любые дубликаты, так как ID на странице должен быть один
        self.name_input = page.locator("#name-input")
        self.email_input = page.locator("#email")     # У этого поля ID просто 'email'
        self.message_input = page.locator("#message") # У этого поля ID 'message'
        self.submit_btn = page.locator("#submit-btn")

    def fill_form(self, name, email, message="Testing Mocking"):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.message_input.fill(message)
        
    def submit(self):
        self.submit_btn.click()