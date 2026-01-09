from playwright.sync_api import Page

class DelayPage:  # ПРОВЕРЬ ЭТУ СТРОКУ
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://practice-automation.com/javascript-delays/"
        self.start_btn = page.locator("#start")
        self.result_text = page.locator("#delay")

    def navigate(self):
        print(f"\n[INFO] Пытаюсь прорваться на {self.url}...")
        try:
            self.page.goto(self.url, wait_until="domcontentloaded", timeout=20000)
        except Exception as e:
            print(f"[WARNING] Сайт тормозит: {e}")
            self.page.evaluate("window.stop()")

    def click_start(self):
        self.start_btn.click()