from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

from utils.db_utils.connect_db import cursor, connect
from utils.db_utils.db_functions import continents_convert

from utils.misc.continents_data import data_continents


@dp.message_handler(Command("my_statistic"))
async def my_statistic(message: types.Message):
    text = f"<b>Статистика пользователя {message.from_user.username} в тесте по " \
           f"столицам стран разных континетов 🏔:</b>\n\n"

    for continent in list(data_continents.keys()):
        cursor.execute(f"""SELECT {continents_convert[continent]} FROM users WHERE id = {message.from_user.id};""")
        points = cursor.fetchone()[0]

        text = text + f"<b>{continent}: максимум {points} верных ответов.</b>\n\n"

    await message.answer(text)

