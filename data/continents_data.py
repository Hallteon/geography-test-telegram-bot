from utils.scrappers import countries_scrapper
import asyncio

loop = asyncio.get_event_loop()
continents_data = loop.run_until_complete(countries_scrapper())