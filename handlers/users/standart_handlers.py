from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from loader import dp, bot
from utils.db_utils.db_functions import create_user_record


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    bot_name = await dp.bot.get_me()
    user_name = message.from_user.username

    text = f"👋 <b>{user_name}, привет! @{bot_name.username} 🤖 - это бот, с помощью " \
           f"которого можно учить столицы стран мира 🌍 " \
           f"в формате теста 📝\nВведи / или отправь команду /help " \
           f"чтобы увидеть доступные команды этого бота ✅</b>"

    await message.answer(text)
    await create_user_record(message.from_user.id, message.from_user.username)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = "Доступные команды бота ✏:\n" \
           "/test - открыть меню теста по столицам стран."

    await message.answer(text)
