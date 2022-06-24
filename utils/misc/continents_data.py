from utils.misc.scrappers import countries_scrapper
import asyncio

loop = asyncio.get_event_loop()
data_continents = loop.run_until_complete(countries_scrapper())