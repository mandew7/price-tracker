import os
from playwright.async_api import async_playwright
from app.parser.base import BaseParser

class CyberportParser(BaseParser):
    def __init__(self, query: str):
        super().__init__(query)
        self.base_url = "https://www.cyberport.de"
        self.country = "DE"

    async def get_data(self):
        store_name = "Cyberport DE"
        print(f"[{store_name}] 🚀 Запуск браузера...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Формируем ПОЛНУЮ ссылку
                search_url = f"{self.base_url}/search.html?query={self.query.replace(' ', '+')}"
                print(f"[{store_name}] 🔍 Поиск товара: {search_url}")
                
                await page.goto(search_url, wait_until="domcontentloaded", timeout=60000)
                
                # Селектор ссылки на товар в списке выдачи
                product_link_selector = "article a.product-card__link"
                print(f"[{store_name}] ⏳ Жду выдачу поиска...")
                await page.wait_for_selector(product_link_selector, timeout=15000)
                
                product_url = await page.get_attribute(product_link_selector, "href")
                
                if product_url and not product_url.startswith("http"):
                    product_url = self.base_url + product_url

                print(f"[{store_name}] ✅ Нашел товар, открываю страницу: {product_url}")
                await page.goto(product_url, wait_until="domcontentloaded")
                
                print(f"[{store_name}] 📊 Извлекаю цену...")
                title = await page.inner_text("h1")
                # В Cyberport цена обычно находится в элементе с этим классом
                price_text = await page.inner_text(".price__value")
                
                print(f"[{store_name}] ✨ Сбор данных завершен!")
                await browser.close()
                return {
                    "store": "Cyberport",
                    "country": self.country,
                    "title": title.strip(),
                    "price": self.clean_price(price_text),
                    "url": product_url,
                    "status": "success"
                }
            except Exception as e:
                print(f"[{store_name}] ❌ ОШИБКА: {str(e)}")
                os.makedirs("debug_screens", exist_ok=True)
                await page.screenshot(path="debug_screens/cyberport_error.png")
                await browser.close()
                return {"store": "Cyberport", "error": str(e)}