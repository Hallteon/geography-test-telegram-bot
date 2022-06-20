import random

from aiogram.dispatcher import FSMContext

from filters import IsInStatesGroup
from utils.inline_keyboards import main_menu, choice_menu, data, next_menu, create_question_menu, start_menu
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp

from states import Test


@dp.message_handler(Command("test"))
async def bot_test(message: types.Message):
    await message.answer(f"Чтобы пройти тест по столицам стран, выберите континент 🏝\n",
                         reply_markup=main_menu)


@dp.callback_query_handler(text="choice")
async def choice_continent(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите континент, по столицам странам которого "
                                     "будет проводиться тест 🏝")
    await callback.message.edit_reply_markup(reply_markup=choice_menu)

    await Test.first()


@dp.callback_query_handler(text_contains="choice_continent", state=Test.start)
async def start_test(callback: types.CallbackQuery, state: FSMContext):
    continent = callback.data.split(":")[-1]
    countries = data[continent]

    await callback.message.edit_text(f"Выбран континент: <b>{continent}</b> ⛰")
    await callback.message.edit_reply_markup(reply_markup=start_menu)

    async with state.proxy() as data_test:
        data_test["continent"] = continent
        data_test["countries"] = countries

    await Test.next()


@dp.callback_query_handler(text="back", state=Test.Q1)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await choice_continent(callback)


@dp.callback_query_handler(IsInStatesGroup(), text="start_question")
async def start_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()
    countries = data_test["countries"]

    country = str(random.choice(list(countries.keys())))

    await callback.message.edit_text(f"<b>Выберите столицу страны: {country}.</b>")
    await callback.message.edit_reply_markup(reply_markup=await create_question_menu(country, countries))

    async with state.proxy() as data:
        data["country"] = country
        data["countries"] = countries

    await Test.next()


@dp.callback_query_handler(IsInStatesGroup(), text_contains="question:correct")
async def correct_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test['country']
    capital = data_test['countries']['country']

    await callback.message.edit_text(f"Вы ответили правильно ✅.\n{capital} - "
                                     f"столица страны {country}.")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]


@dp.callback_query_handler(IsInStatesGroup(), text_contains="question:incorrect")
async def incorrect_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test["country"]
    right_capital = data_test["countries"]["country"]
    wrong_capital = callback.data.split(":")[2]

    await callback.message.edit_text(f"Вы ответили неправильно ❌.\n{right_capital} - "
                                     f"столица страны {country}.\nВаш ответ: "
                                     f"{wrong_capital}")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]


@dp.callback_query_handler(IsInStatesGroup(), text="next_question")
async def next_question(callback: types.CallbackQuery, state: FSMContext):
    await start_question(callback, state)

