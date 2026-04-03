import asyncio
from app.parser.mediamarkt import MediaMarktParser

async def main():
    url = "https://www.mediamarkt.de/de/product/_philips-65pus9000-qled-ambilight-tv-flat-65-zoll-164-cm-uhd-4k-smart-tv-ambilight-2982249.html"
    parser = MediaMarktParser(url)
    result = await parser.get_data()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())