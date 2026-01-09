from playwright.sync_api import Page, expect
from pages.modals_page import ModalsPage
from faker import Faker

def test_modal_with_form_and_alert(page: Page):
    faker = Faker()
    modals_page = ModalsPage(page)
    modals_page.navigate()

    name = faker.name()
    email = faker.email()

    # Открываем и заполняем
    modals_page.fill_form_in_modal(name, email)

    # --- ДОБАВЬ ЭТИ СТРОКИ ДЛЯ ПРОВЕРКИ ---
    print(f"Ввел данные: {name}, {email}")
    page.wait_for_timeout(1000) # Пауза на 1 секунду, чтобы ты успел увидеть
    page.screenshot(path="debug_modal_fill.png") # Делаем проверочный скриншот
    # -------------------------------------

    # Обработка Alert (нажмет ОК автоматически)
    page.on("dialog", lambda dialog: print(f"Вижу Alert: {dialog.message}") or dialog.accept())

    # Нажимаем Submit
    modals_page.modal_submit_btn.click()