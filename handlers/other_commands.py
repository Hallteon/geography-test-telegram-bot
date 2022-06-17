from utils.throttling import rate_limit
from aiogram import types
from aiogram.dispatcher.filters import Command

from utils import scrappers
from loader import dp, bot


@dp.message_handler(Command("test"))
async def bot_test(message: types.Message):
    data = await scrappers.countries_scrapper()

    await message.answer(f"Hello!")
