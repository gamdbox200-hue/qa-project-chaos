import pytest
import requests
import allure
import psycopg2
from typing import Generator
from utils.db_handler import DBHandler
from playwright.sync_api import Playwright, APIRequestContext, Page
import base64
from faker import Faker
# Импортируем твои классы страниц (убедись, что пути к файлам верны)
from pages.modals_page import ModalsPage
from pages.slider_page import SliderPage
from pages.users_page import UsersPage
from api.posts_client import PostsClient

# --- БЛОК ПОДГОТОВКИ ТЕСТОВ (FIXTURES) ---

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture
def posts_api(base_url):
    return PostsClient(base_url)

@pytest.fixture
def db_session():
    # SETUP: Подключаемся к базе
    db = DBHandler()
    yield db  # Здесь запускается сам тест
    # TEARDOWN: После теста закрываем всё
    db.close()

@pytest.fixture
def temp_post(db_session):
    """Фикстура, которая сама создает пост и САМА его удаляет"""
    title = "Fixture Managed Post"
    
    # 1. Создаем
    db_session.create_post(title, "Content from Fixture", 1)
    
    yield title  # Передаем название поста в тест
    
    # 2. Удаляем (выполнится автоматически после теста)
    db_session.delete_post_by_title(title)







@pytest.fixture(scope="session")
def fake():
    """Глобальный генератор случайных данных"""
    return Faker()

@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(
        dbname="qa_db", 
        user="admin", 
        password="password", 
        host="localhost"
    )
    yield conn
    conn.close()


@pytest.fixture
def modals_page(page: Page):
    page_obj = ModalsPage(page)
    # Ждем только загрузки DOM, а не всех тяжелых ресурсов
    page.goto("https://practice-automation.com/modals/", wait_until="domcontentloaded") 
    return page_obj

@pytest.fixture
def slider_page(page):
    """Фикстура для страницы со слайдером"""
    page_obj = SliderPage(page)
    page.goto("https://practice-automation.com/slider/")
    return page_obj


# --- БЛОК ОТЧЕТНОСТИ И СКРИНШОТОВ (HOOKS) ---

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        # Пытаемся достать объект 'page' из аргументов теста
        page = item.funcargs.get("page")
        if page:
            # Делаем скриншот
            screenshot_bytes = page.screenshot(full_page=False)
            screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")
            
            # Вставляем красивый HTML-блок в отчет
            html = (
                '<div>'
                f'<img src="data:image/png;base64,{screenshot_base64}" '
                'style="width:600px; border:2px solid #ddd; border-radius:5px; margin-top:10px;" '
                'onclick="window.open(this.src)">'
                '<p style="color:gray; font-size:12px;">(Кликните по картинке, если нужно открыть в полный размер в новой вкладке)</p>'
                '</div>'
            )
            extras.append(pytest_html.extras.html(html))
        report.extras = extras

@pytest.fixture
def api_client(request):
    # Пытаемся взять base_url из конфига pytest.ini напрямую
    base_addr = request.config.getini("base_url")
    
    # Если в ini пусто, попробуем взять из параметров командной строки (плагин)
    if not base_addr:
        base_addr = request.config.getoption("base_url", default=None)

    if not base_addr or base_addr == "None":
        pytest.fail("Base URL не определен! Проверьте секцию [pytest] в pytest.ini")

    class Client:
        def __init__(self, addr):
            self.addr = addr
        def get(self, endpoint, **kwargs):
            return requests.get(f"{self.addr}{endpoint}", **kwargs)
        def post(self, endpoint, json=None, **kwargs):
            return requests.post(f"{self.addr}{endpoint}", json=json, **kwargs)

    return Client(base_addr)

@pytest.fixture
def form_page(page):
    from pages.form_page import FormPage
    
    # Устанавливаем таймаут ожидания загрузки (60 секунд)
    page.set_default_navigation_timeout(60000)
    # Устанавливаем таймаут для действий типа click, fill (30 секунд)
    page.set_default_timeout(30000)
    
    form_page_obj = FormPage(page)
    # Используем commit, чтобы не ждать тяжелые скрипты аналитики
    with allure.step ("Открыть страницу с формами"):
        (page.goto("https://practice-automation.com/form-fields/", wait_until="commit"))
    return form_page_obj

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    request_context = playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield request_context
    request_context.dispose()

@pytest.fixture
def users_page(page: Page) -> UsersPage:
    return UsersPage(page)

@pytest.fixture
def fake():
    return Faker() # Можно указать локаль, например Faker('ru_RU')