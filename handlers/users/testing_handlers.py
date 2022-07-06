import random

from aiogram.dispatcher import FSMContext

from utils.db_utils.db_functions import set_max_continent_points
from utils.misc.create_flages_emojies import create_flag
from utils.inline_keyboards import main_menu, choice_menu, geo_data, next_menu, create_question_menu, start_menu

from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp

from states import Test
from utils.misc.throttling import rate_limit


@rate_limit(5)
@dp.message_handler(Command("test"))
async def bot_test(message: types.Message):
    await message.answer(f"<b>Нажмите на первую кнопку для выбора континента 🏝\n"
                         f"На вторую для выхода из теста 📝</b>",
                         reply_markup=main_menu)


@dp.callback_query_handler(text="exit")
async def exit_from_test(callback: types.CallbackQuery):
    await callback.message.delete()


@dp.callback_query_handler(text="choice")
async def choice_continent(callback: types.CallbackQuery):
    await callback.message.edit_text("<b>Выберите континент, по столицам странам которого "
                                     "будет проводиться тест</b> 📝")
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
        data_test["counter"] = 0

    await Test.next()


@dp.callback_query_handler(text="back", state=Test.question)
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await choice_continent(callback)


@dp.callback_query_handler(state=Test.question, text="start_question")
async def start_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    all_countries = data_test["countries"]

    country = str(random.choice(list(all_countries.keys())))

    await callback.message.edit_text(f"Выберите столицу страны: <b>{country}</b> {await create_flag(country)}")
    await callback.message.edit_reply_markup(reply_markup=await create_question_menu(country, all_countries))

    async with state.proxy() as data:
        data["country"] = country
        data["countries"] = all_countries
        data["counter"] += 1


@dp.callback_query_handler(text_contains="question:correct", state=Test.question)
async def correct_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test['country']
    capital = data_test['countries'][country]

    await callback.message.edit_text(f"<b>Вы ответили правильно</b> ✅\n<b>{capital}</b> - "
                                     f"столица страны <b>{country}</b> {await create_flag(country)}")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]
        data["correct"] += 1

    if data["counter"] == 10:
        await state.set_state(Test.result)


@dp.callback_query_handler(text_contains="question:incorrect", state=Test.question)
async def incorrect_question(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    country = data_test["country"]
    right_capital = data_test["countries"][country]

    await callback.message.edit_text(f"<b>Вы ответили неправильно</b> ❌\n<b>{right_capital}</b> - "
                                     f"столица страны <b>{country}</b> {await create_flag(country)}")
    await callback.message.edit_reply_markup(reply_markup=next_menu)

    async with state.proxy() as data:
        del data["countries"][country]

    if data["counter"] == 10:
        await state.set_state(Test.result)


@dp.callback_query_handler(state=Test.result)
async def return_results(callback: types.CallbackQuery, state: FSMContext):
    data_test = await state.get_data()

    continent = data_test["continent"]
    correct_questions = data_test["correct"]

    await callback.message.edit_text(f"<b>Вы завершили тест по странам континента"
                                     f" {continent} ⛰\nПравильных ответов - "
                                     f"{correct_questions} ✅\nВсего вопросов - "
                                     f"{data_test['counter']} ❔</b>")
    await set_max_continent_points(callback.from_user.id, continent, correct_questions)

    await state.reset_state()


@dp.callback_query_handler(text="next_question", state=Test.all_states[1:])
async def next_question(callback: types.CallbackQuery, state: FSMContext):
    await start_question(callback, state)

