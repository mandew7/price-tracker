import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from app.parser.base import BaseParser

class MediaMarktParser(BaseParser):
    async def get_data(self):
        async with async_playwright() as p:
            # Запускаем браузер
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Применяем стелс через правильный метод, который мы нашли
            stealth_config = Stealth()
            await stealth_config.apply_stealth_async(page) 
            
            try:
                # Переходим на сайт
                # Используем wait_until="domcontentloaded", так как MediaMarkt тяжелый
                await page.goto(self.url, wait_until="domcontentloaded", timeout=60000)
                
                # Ждем появления заголовка h1
                await page.wait_for_selector("h1", timeout=30000)
                
                title = await page.inner_text("h1")
                
                await browser.close()
                return {
                    "title": title.strip(),
                    "status": "success"
                }
            except Exception as e:
                # Если не сработало — делаем скриншот, чтобы понять причину (капча или блок)
                await page.screenshot(path="mediamarkt_debug.png")
                await browser.close()
                return {"error": str(e)}