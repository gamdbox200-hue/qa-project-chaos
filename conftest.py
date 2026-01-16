import pytest
import requests
import allure
import psycopg2
import base64
from typing import Generator, AsyncGenerator
from utils.db_handler import DBHandler
from faker import Faker
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, APIRequestContext, Playwright

# Импорты твоих страниц и клиентов
from pages.modals_page import ModalsPage
from pages.slider_page import SliderPage
from pages.users_page import UsersPage
from pages.form_page import FormPage  # добавь, если используешь
from api.posts_client import PostsClient

# --- PLAYWRIGHT ASYNC FIXTURES (новые, заменяют sync) ---

@pytest.fixture(scope="session")
async def playwright() -> AsyncGenerator[Playwright, None]:
    """Запускает Playwright один раз на сессию"""
    pw = await async_playwright().start()
    yield pw
    await pw.stop()


@pytest.fixture(scope="session")
async def browser(playwright: Playwright) -> AsyncGenerator[Browser, None]:
    """Браузер Chromium на сессию (можно добавить firefox/webkig)"""
    browser = await playwright.chromium.launch(
        headless=True,  # False для дебага локально
        args=["--no-sandbox", "--disable-setuid-sandbox"]  # для CI/Docker
    )
    yield browser
    await browser.close()


@pytest.fixture(scope="session")
async def browser_context_args() -> dict:
    """Передаём viewport и другие настройки контекста"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "locale": "en-US",
        "timezone_id": "Europe/Warsaw",  # под Pomerania/PL
    }


@pytest.fixture(scope="function")
async def context(
    browser: Browser,
    browser_context_args: dict
) -> AsyncGenerator[BrowserContext, None]:
    """Новый контекст на каждый тест (изолированный)"""
    ctx = await browser.new_context(**browser_context_args)
    yield ctx
    await ctx.close()


@pytest.fixture(scope="function")
async def page(context: BrowserContext) -> AsyncGenerator[Page, None]:
    """Новая страница на каждый тест"""
    page = await context.new_page()
    # Устанавливаем дефолтные таймауты
    page.set_default_timeout(30000)          # 30 сек на действия
    page.set_default_navigation_timeout(60000)  # 60 сек на goto
    yield page
    await page.close()


# --- ТВОИ СТАРЫЕ ФИКСТУРЫ (оставляем почти без изменений) ---

@pytest.fixture
def posts_api(base_url):
    return PostsClient(base_url)


@pytest.fixture(scope="session")
def db_handler():
    handler = DBHandler()
    yield handler
    handler.close()


@pytest.fixture(scope="function")
def db_session(db_handler):
    # Можно добавить очистку таблиц перед тестом
    # db_handler.clear_tables()
    yield db_handler


@pytest.fixture
def temp_post(db_session):
    title = "Fixture Managed Post"
    db_session.create_post(title, "Content from Fixture", 1)
    yield title
    db_session.delete_post_by_title(title)


@pytest.fixture(scope="session")
def fake():
    return Faker('ru_RU')  # можно 'en_US' или 'pl_PL'


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


# --- POM ФИКСТУРЫ (обновляем под async page) ---

@pytest.fixture
async def modals_page(page: Page) -> ModalsPage:
    page_obj = ModalsPage(page)
    await page.goto("https://practice-automation.com/modals/", wait_until="domcontentloaded")
    return page_obj


@pytest.fixture
async def slider_page(page: Page) -> SliderPage:
    page_obj = SliderPage(page)
    await page.goto("https://practice-automation.com/slider/")
    return page_obj


@pytest.fixture
async def form_page(page: Page) -> FormPage:
    page_obj = FormPage(page)
    await page.goto("https://practice-automation.com/form-fields/", wait_until="commit")
    return page_obj


@pytest.fixture
def users_page(page: Page) -> UsersPage:
    return UsersPage(page)


# --- API ФИКСТУРА (остаётся sync, но можно сделать async если нужно) ---

@pytest.fixture(scope="session")
async def api_request_context(playwright: Playwright) -> AsyncGenerator[APIRequestContext, None]:
    ctx = await playwright.request.new_context(
        base_url="https://jsonplaceholder.typicode.com"
    )
    yield ctx
    await ctx.dispose()


# --- Allure + СКРИНШОТЫ (обновляем под async) ---

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        # Берём page из теста (если он есть)
        page = item.funcargs.get("page")
        if page and hasattr(page, "screenshot"):  # async page
            try:
                # Для async: нужно await, но в hook'е мы не можем await напрямую
                # Решение: делаем скрин в самом тесте или используем sync-обёртку
                # Пока — простой способ: если тест async — скрин в тесте
                pass
            except Exception as e:
                print(f"Screenshot failed: {e}")

        # Альтернатива: скриншоты лучше делать В САМИХ ТЕСТАХ (await page.screenshot())
        # Пример в тесте:
        # await page.screenshot(path="error.png")
        # allure.attach.file("error.png", name="Screenshot", attachment_type=allure.attachment_type.PNG)

    report.extras = extras


# --- Дополнительно: базовый URL из ini или CLI ---

@pytest.fixture
def api_client(request):
    base_addr = request.config.getini("base_url") or request.config.getoption("base_url", default=None)
    if not base_addr or base_addr == "None":
        pytest.fail("Base URL не определен! Укажи в pytest.ini или --base-url")
    
    class Client:
        def __init__(self, addr):
            self.addr = addr
        def get(self, endpoint, **kwargs):
            return requests.get(f"{self.addr}{endpoint}", **kwargs)
        def post(self, endpoint, json=None, **kwargs):
            return requests.post(f"{self.addr}{endpoint}", json=json, **kwargs)

    return Client(base_addr)