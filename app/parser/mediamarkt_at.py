from app.parser.mediamarkt import MediaMarktParser

# ВАЖНО: Имя класса должно быть именно таким, как в ошибке
class MediaMarktATParser(MediaMarktParser):
    def __init__(self, query: str):
        super().__init__(query)
        self.base_url = "https://www.mediamarkt.at"
        self.country = "AT"
    
    # Метод get_data подтянется автоматически из твоего кода выше