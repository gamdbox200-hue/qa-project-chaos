# tests/test_login.py
import pytest
from playwright.async_api import Page, expect
from pages.your_login_page import LoginPage  # если есть POM

@pytest.mark.asyncio
async def test_successful_login(page: Page):
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.get_by_label("Username").fill("tomsmith")
    await page.get_by_placeholder("Password").fill("SuperSecretPassword!")
    await page.get_by_role("button", name="Login").click()

    success_msg = page.get_by_text("You logged into a secure area!")
    await expect(success_msg).to_be_visible()

    # Скриншот + Allure (лучше здесь!)
    screenshot_path = "success_login.png"
    await page.screenshot(path=screenshot_path)
    allure.attach.file(screenshot_path, name="Success Login", attachment_type=allure.attachment_type.PNG)