from playwright.sync_api import Page, expect
from delay_page import DelayPage

def test_javascript_delay(page: Page):
    delay_page = DelayPage(page)
    delay_page.navigate()

    # Ждем кнопку перед кликом (на всякий случай)
    delay_page.start_btn.wait_for(state="visible", timeout=5000)

    # 1. Нажимаем кнопку
    delay_page.click_start()

    # 2. Ждем и проверяем результат (10 секунд ожидания сайта + наш запас)
    print("Нажали старт, ждем 10 секунд... Мишка Домингос спокоен...")
    expect(delay_page.result_text).to_have_text("Liftoff!", timeout=15000)
    
    print("Победа! Мы дождались JS-задержки.")