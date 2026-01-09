from playwright.sync_api import Page

class SliderPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://practice-automation.com/slider/"
        self.slider = page.locator('input[type="range"]') 
        self.value_text = page.locator("#value")

    def navigate(self):
        print(f"\n[INFO] Пытаюсь прорваться на {self.url}...")
        try:
            # Используем commit для скорости
            self.page.goto(self.url, wait_until="commit", timeout=20000)
        except Exception as e:
            print(f"[WARNING] Ошибка при загрузке: {e}")

    # ВОТ ЭТОТ МЕТОД НУЖНО ВЕРНУТЬ:
    def set_slider_value(self, target_value):
        # Двигаем ползунок через JavaScript (самый надежный метод)
        self.slider.evaluate(f"(node) => node.value = {target_value}")
        # Генерируем событие, чтобы сайт увидел изменения
        self.slider.dispatch_event("input")