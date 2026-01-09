from playwright.sync_api import expect

def test_simple_modal_popup(modals_page): # Используем фикстуру вместо (page)
    # Тест сразу знает про modals_page и уже находится на нужной странице
    
    # Открываем модалку
    modals_page.open_simple_modal()

    # ПРОВЕРКА
    expect(modals_page.modal_header).to_be_visible()