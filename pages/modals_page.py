from playwright.sync_api import Page

class ModalsPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://practice-automation.com/modals/"
        
        # Элементы для Simple Modal
        self.simple_modal_btn = page.locator("#simpleModal")
        self.modal_header = page.locator("#pum_popup_title_1318") # Уточним локатор заголовка
        self.close_btn = page.locator(".pum-close").filter(has_text="×")
        
        # Элементы для Form Modal
        self.form_modal_btn = page.locator("#formModal")
        self.modal_name_input = page.locator("#g1051-name")
        self.modal_email_input = page.locator("#g1051-email")
        self.modal_submit_btn = page.locator("button:has-text('Submit')")

    def navigate(self):
        # Добавляем таймаут и стратегию ожидания для стабильности
        self.page.goto(self.url, wait_until="domcontentloaded", timeout=30000)

    # ВОТ ЭТОТ МЕТОД МЫ ПОТЕРЯЛИ:
    def open_simple_modal(self):
        self.simple_modal_btn.click()

    # А этот для формы:
    def fill_form_in_modal(self, name, email):
        self.form_modal_btn.click()
        self.modal_name_input.fill(name)
        self.modal_email_input.fill(email)