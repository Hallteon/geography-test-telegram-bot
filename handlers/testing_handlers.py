import random

from aiogram.dispatcher import FSMContext

from filters import IsInStatesGroup
from utils.inline_keyboards import main_menu, choice_menu, geo_data, next_menu, create_question_menu, start_menu
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp, storage

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
    countries = geo_data[continent]

    await callback.message.edit_text(f"Выбран континент: <b>{continent}</b> ⛰")
    await callback.message.edit_reply_markup(reply_markup=start_menu)

    async with state.proxy() as data_test:
        data_test["continent"] = continent
        data_test["countries"] = countries
        data_test["correct"] = 0

    await Test.next()


@dp.callback_query_handler(state=Test.Q1, text="back")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await choice_continent(callback)


@dp.callback_query_handler(state=Test.all_states[1:-1], text="start_question")
async def start_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    all_countries = data_test["countries"]

    country = str(random.choice(list(all_countries.keys())))

    await callback.message.edit_text(f"<b>Выберите столицу страны: {country}.</b>")
    await callback.message.edit_reply_markup(reply_markup=await create_question_menu(country, all_countries))

    async with state.proxy() as data:
        data["country"] = country
        data["countries"] = all_countries

    await Test.next()


@dp.callback_query_handler(state=Test.all_states[1:], text_contains="question:correct")
async def correct_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test['country']
    capital = data_test['countries'][country]

    await callback.message.edit_text(f"<b>Вы ответили правильно ✅.\n{capital} - "
                                     f"столица страны {country}.</b>")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]
        data["correct"] += 1


@dp.callback_query_handler(state=Test.all_states[1:], text_contains="question:incorrect")
async def incorrect_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test["country"]
    right_capital = data_test["countries"][country]

    await callback.message.edit_text(f"<b>Вы ответили неправильно ❌.\n{right_capital} - "
                                     f"столица страны {country}.</b>")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]


@dp.callback_query_handler(state=Test.result)
async def return_results(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    continent = data_test["continent"]
    correct_questions = data_test["correct"]

    await callback.message.edit_text(f"<b>Вы завершили тест по странам континента"
                                     f" {continent} ⛰. Правильных ответов - "
                                     f"{correct_questions} ✅. Всего вопросов - "
                                     f"{len(Test.all_states_names[1:-1])}.</b>")
    await state.reset_state()


@dp.callback_query_handler(state=Test.all_states[1:], text="next_question")
async def next_question(callback: types.CallbackQuery, state: FSMContext):
    await start_question(callback, state)

