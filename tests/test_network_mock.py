import json
from playwright.sync_api import expect

def test_mock_page_content(page):
    # 1. Настройка: увеличим таймаут для слабых сетей
    page.set_default_navigation_timeout(60000)

    # 2. ДИВЕРСИЯ: Мы не меняем HTML, мы внедряем скрипт, 
    # который изменит страницу СРАЗУ после загрузки DOM
    def inject_javascript(route):
        response = route.fetch()
        # Добавляем в конец HTML-кода наш "злой" скрипт
        payload = """
        <script>
        window.addEventListener('DOMContentLoaded', () => {
            document.body.innerHTML = document.body.innerHTML.replace(/Name/g, '⚠️ SYSTEM COMPROMISED');
            document.body.style.backgroundColor = 'black';
            document.body.style.color = '#00FF00';
            document.querySelectorAll('label').forEach(el => el.style.color = '#00FF00');
        });
        </script>
        """
        new_body = response.text().replace("</body>", f"{payload}</body>")
        
        route.fulfill(response=response, body=new_body)

    page.route("**/form-fields/", inject_javascript)

    # 3. ПЕРЕХОД
    page.goto("https://practice-automation.com/form-fields/", wait_until="commit")

    # 4. ПРОВЕРКА (с небольшим ожиданием, пока отработает JS)
    # Используем более гибкий поиск
    locator = page.get_by_text("SYSTEM COMPROMISED").first
    expect(locator).to_be_visible(timeout=10000)
    
    print("\n✅ МАТРИЦА АКТИВИРОВАНА!")
    page.wait_for_timeout(5000)