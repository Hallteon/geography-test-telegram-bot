from aiogram import types
from aiogram.dispatcher.filters import Command

from filters import IsAdmin
from loader import dp
from utils.db_utils.connect_db import cursor
from utils.db_utils.db_functions import continents_convert
from utils.misc.continents_data import data_continents


@dp.message_handler(IsAdmin(), Command("statistic"))
async def statistic(message: types.Message):
    user_id = message.get_args().split()

    if user_id:
        user_id = user_id[0]

        try:
            cursor.execute(f"""SELECT name FROM users WHERE id = {user_id};""")

        except:
            await message.answer("<b>Не существует пользователя с таким id!</b>")

        else:
            text = f"<b>Статистика пользователя {cursor.fetchone()[0]} в тесте по " \
                   f"столицам стран разных континетов 🏔:</b>\n\n"

            for continent in list(data_continents.keys()):
                cursor.execute(f"""SELECT {continents_convert[continent]} FROM users WHERE id = {user_id};""")
                points = cursor.fetchone()[0]

                text = text + f"<b>{continent}: максимум {points} верных ответов.</b>\n\n"

            await message.answer(text)

    else:
        await message.answer("<b>Вы забыли передать id пользователя!</b>")