from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseParser(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    async def get_data(self) -> Dict[str, Any]:
        """
        Метод должен вернуть словарь:
        {
            "title": str,
            "price": float,
            "category": str,
            "attributes": dict  # Здесь будут веса, бренды и т.д.
        }
        """
        pass