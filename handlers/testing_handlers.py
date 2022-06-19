import random

from utils.inline_keyboards import main_menu, choice_menu, create_start_menu, create_question_menu, data, next_menu
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, bot


@dp.message_handler(Command("test"))
async def bot_test(message: types.Message):
    await message.answer(f"Чтобы пройти тест по столицам стран, выберите континент 🏝\n",
                         reply_markup=main_menu)


@dp.callback_query_handler(text="choice")
async def choice_continent(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите континент, по столицам странам которого "
                                     "будет проводиться тест 🏝")
    await callback.message.edit_reply_markup(reply_markup=choice_menu)


@dp.callback_query_handler(text_contains="choice_continent")
async def start_test(callback: types.CallbackQuery):
    name = callback.data.split(":")[-1]

    start_menu = await create_start_menu(name)

    await callback.message.edit_text(f"Выбран континент: <b>{name}</b> ⛰")
    await callback.message.edit_reply_markup(reply_markup=start_menu)


@dp.callback_query_handler(text="back")
async def back_to_menu(callback: types.CallbackQuery):
    await choice_continent(callback)


@dp.callback_query_handler(text_contains="start_quest")
async def start_question(callback: types.CallbackQuery):
    continent = callback.data.split(":")[-1]
    country = str(random.choice(list(data[continent].keys())))

    await callback.message.edit_text(f"<b>Выберите столицу страны: {country}.</b>")
    await callback.message.edit_reply_markup(reply_markup=await create_question_menu(continent, country))


@dp.callback_query_handler(text_contains="question:correct")
async def correct_question(callback: types.CallbackQuery):
    continent = callback.data.split(":")[2]
    country = callback.data.split(":")[3]

    await callback.message.edit_text(f"Вы ответили правильно ✅.\n{data[continent][country]} - "
                                     f"столица страны {country}.")
    await callback.message.edit_reply_markup(reply_markup=next_menu)


@dp.callback_query_handler(text_contains="question:incorrect")
async def incorrect_question(callback: types.CallbackQuery):
    continent = callback.data.split(":")[2]
    country = callback.data.split(":")[3]

    await callback.message.edit_text(f"Вы ответили неправильно ❌.\n{data[continent][country]} - "
                                     f"столица страны {country} 🏘.")
    await callback.message.edit_reply_markup(reply_markup=next_menu)


@dp.callback_query_handler(text="next_question")
async def next_question(callback: types.CallbackQuery):
    await start_question(callback)

