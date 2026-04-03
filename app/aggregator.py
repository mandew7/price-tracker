import asyncio

class ProductAggregator:
    def __init__(self, query: str):
        self.query = query
        self.parsers = []

    def add_parser(self, parser_class):
        self.parsers.append(parser_class(self.query))

    async def run(self):
        print(f"🔎 Ищем: {self.query}...")
        tasks = [parser.get_data() for parser in self.parsers]
        results = await asyncio.gather(*tasks)
        
        # Фильтруем ошибки и сортируем по цене
        valid_results = [r for r in results if "error" not in r]
        sorted_results = sorted(valid_results, key=lambda x: x['price'])
        
        return sorted_results