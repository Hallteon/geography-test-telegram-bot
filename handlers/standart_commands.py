from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    bot_name = await dp.bot.get_me()

    await message.answer(f"Привет, <b>{message.chat.username}</b>! "
                         f"<b>{bot_name.username}</b> - это бот "
                         f"для получения информации об актуальных скидках "
                         f"и акциях в интернет-магазинах книг "
                         f"<b>Читай Город</b>, <b>Book24</b> и "
                         f"<b>Лабиринт</b>.")


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "<b>Список доступных команд:</b>\n" \
           "/help - <i>вывести данные о командах.</i>\n" \
           "/sales - <i>посмотреть акции и скидки в выбранном " \
           "книжном интернет-магазине.</i>"

    await message.answer(text)