import asyncio
import json
from app.aggregator import ProductAggregator
from app.parser.mediamarkt import MediaMarktParser
# Остальные импорты можно оставить или закомментировать
# from app.parser.mediamarkt_at import MediaMarktATParser
# from app.parser.cyberport import CyberportParser

async def main():
    # Оставляем один конкретный запрос
    query = "Sony PlayStation 5 Pro" 
    
    aggregator = ProductAggregator(query)
    
    # Добавляем ТОЛЬКО основной MediaMarkt для тестов маскировки
    aggregator.add_parser(MediaMarktParser)
    
    # Эти строки закомментированы (отключены):
    # aggregator.add_parser(MediaMarktATParser)
    # aggregator.add_parser(CyberportParser)
    
    results = await aggregator.run()
    
    print(f"\n🌍 ТЕСТОВЫЙ ЗАПУСК (MediaMarkt DE) для: {query}")
    print("-" * 50)
    
    if not results:
        print("❌ Ничего не найдено или доступ заблокирован.")
    
    for res in results:
        if "error" in res:
            print(f"[{res.get('country', '??')}] {res['store']}: ОШИБКА -> {res['error']}")
        else:
            print(f"[{res['country']}] {res['store']}: {res['price']}€")
            print(f"🔗 {res['url']}\n")

if __name__ == "__main__":
    asyncio.run(main())