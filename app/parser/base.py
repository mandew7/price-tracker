from abc import ABC, abstractmethod

class BaseParser(ABC):
    def __init__(self, query: str):
        self.query = query
        self.base_url = ""
        self.country = "DE" # По умолчанию Германия

    @abstractmethod
    async def get_data(self) -> dict:
        pass

    def clean_price(self, price_str: str) -> float:
        if not price_str: return 0.0
        # Очистка для европейских форматов (1.299,00 -> 1299.00)
        cleaned = price_str.replace('€', '').replace('EUR', '').strip()
        cleaned = cleaned.replace('.', '').replace(',', '.')
        try:
            return float("".join(c for c in cleaned if c.isdigit() or c == '.'))
        except:
            return 0.0