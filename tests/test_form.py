from playwright.sync_api import Page, expect
from pages.form_page import FormPage

def test_user_can_fill_form(form_page, fake):
    # 1. Данные
    random_name = fake.name()
    random_email = fake.email()
    
    # 2. Обработка Alert (Проверка этапа нахождения результата)
    # Создаем список для хранения сообщений из алертов
    alert_messages = []
    form_page.page.on("dialog", lambda dialog: [
        alert_messages.append(dialog.message),
        dialog.accept()
    ])

    # 3. Действие
    form_page.fill_form(random_name, random_email)
    
    # Проверка, что данные в полях перед отправкой верны
    expect(form_page.name_input).to_have_value(random_name)
    
    # 4. Отправка
    form_page.submit_btn.click()

    # 5. ВЕРИФИКАЦИЯ РЕЗУЛЬТАТА
    # Проверяем, что в алерте пришел текст об успехе
    # (обычно там "Message received!" или аналогично)
    assert len(alert_messages) > 0
    assert "Message received!" in alert_messages[0]