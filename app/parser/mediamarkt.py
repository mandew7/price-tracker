import asyncio
import os
import random
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from app.parser.base import BaseParser

class MediaMarktParser(BaseParser):
    def __init__(self, query: str):
        super().__init__(query)
        self.base_url = "https://www.mediamarkt.de"
        self.country = "DE"

    async def get_data(self):
        store_name = f"MediaMarkt {self.country}"
        print(f"[{store_name}] 🚀 Запуск изолированного браузера...")
        
        async with async_playwright() as p:
            # Используем chromium, но с дополнительными аргументами
            browser = await p.chromium.launch(headless=True)
            
            # Создаем чистый контекст с реалистичным разрешением экрана
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080},
                device_scale_factor=1,
            )
            
            # Полная очистка куков и хранилища
            await context.clear_cookies()
            page = await context.new_page()
            
            print(f"[{store_name}] 🛡️ Активация Stealth-режима...")
            stealth_config = Stealth()
            await stealth_config.apply_stealth_async(page)
            
            try:
                # ШАГ 1: Заходим на главную для "прогрева"
                print(f"[{store_name}] 🧼 Куки чисты. Захожу на главную для прогрева...")
                await page.goto(self.base_url, wait_until="networkidle", timeout=60000)
                
                # Имитируем активность человека: легкий скролл
                await page.mouse.wheel(0, 500)
                await asyncio.sleep(random.uniform(2, 4))
                
                # Проверяем, нет ли капчи уже здесь
                if "captcha" in page.url or await page.query_selector("iframe[src*='cloudflare']"):
                    print(f"[{store_name}] ⚠️ ВНИМАНИЕ: Обнаружена капча на главной странице.")
                
                # ШАГ 2: Переходим к поиску
                search_url = f"{self.base_url}/de/search.html?query={self.query.replace(' ', '+')}"
                print(f"[{store_name}] 🔍 Перехожу к поиску: {search_url}")
                
                # Переходим не сразу, а как будто кликнули
                await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(random.uniform(1, 3))
                
                print(f"[{store_name}] ⏳ Ожидаю результаты...")
                product_selector = "a[data-testid='mms-product-card-title']"
                await page.wait_for_selector(product_selector, timeout=20000)
                
                first_product = page.locator(product_selector).first
                product_url = await first_product.get_attribute("href")
                
                if product_url and not product_url.startswith("http"):
                    product_url = self.base_url + product_url
                
                print(f"[{store_name}] ✅ Нашел! Открываю товар...")
                await page.goto(product_url, wait_until="domcontentloaded")
                
                title = await page.inner_text("h1")
                price_text = await page.inner_text("[data-test='mms-price']")
                
                print(f"[{store_name}] ✨ УСПЕХ: {price_text}")
                await browser.close()
                return {
                    "store": store_name,
                    "country": self.country,
                    "title": title.strip(),
                    "price": self.clean_price(price_text),
                    "url": product_url,
                    "status": "success"
                }
            except Exception as e:
                print(f"[{store_name}] ❌ Сбой на этапе: {str(e)}")
                os.makedirs("debug_screens", exist_ok=True)
                path = f"debug_screens/{store_name.lower().replace(' ', '_')}_final_attempt.png"
                await page.screenshot(path=path)
                print(f"[{store_name}] 📸 Дебаг-скриншот сохранен: {path}")
                await browser.close()
                return {"store": store_name, "error": str(e)}