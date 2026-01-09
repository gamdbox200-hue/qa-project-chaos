from playwright.sync_api import Page, expect
from pages.slider_page import SliderPage

def test_slider_movement(page: Page):
    slider_page = SliderPage(page)
    slider_page.navigate() 

    print("[INFO] Жду появления ползунка...")
    slider_page.slider.wait_for(state="attached", timeout=15000)

    # ДЕЙСТВИЕ 1: Ставим 25
    target_1 = 25
    slider_page.set_slider_value(target_1)
    # ПРОВЕРКА 1: Сразу проверяем, что на странице 25
    expect(slider_page.value_text).to_have_text(str(target_1))
    print(f"Проверка 1 пройдена: {target_1}")

    # ДЕЙСТВИЕ 2: Ставим 90
    target_2 = 90
    slider_page.set_slider_value(target_2)
    # ПРОВЕРКА 2: Проверяем, что теперь 90
    expect(slider_page.value_text).to_have_text(str(target_2))
    print(f"Проверка 2 пройдена: {target_2}")
    
    page.screenshot(path="slider_final_result.png")