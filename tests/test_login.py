# tests/test_login.py — минимальная версия без сторонних страниц

import pytest
from playwright.async_api import Page, expect

@pytest.mark.asyncio
async def test_successful_login(page: Page):
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.get_by_label("Username").fill("tomsmith")
    await page.get_by_placeholder("Password").fill("SuperSecretPassword!")
    await page.get_by_role("button", name="Login").click()

    success_msg = page.get_by_text("You logged into a secure area!")
    await expect(success_msg).to_be_visible(timeout=10000)

    # Скриншот + Allure (если Allure настроен)
    screenshot_path = "screenshots/success_login.png"
    await page.screenshot(path=screenshot_path)
    # allure.attach.file(screenshot_path, name="Success Login", attachment_type=allure.attachment_type.PNG)