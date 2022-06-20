import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.continents_data import continents_data

data = continents_data

choice_callback_data = CallbackData("choice_continent", "continent")
question_callback_data = CallbackData("question", "type", "capital")

continents = list(data.keys())

main_menu = InlineKeyboardMarkup()
main_menu.insert(InlineKeyboardButton(text="Выбрать континент 🏔", callback_data="choice"))

choice_menu = InlineKeyboardMarkup()

for name in continents:
    choice_menu.insert(InlineKeyboardButton(text=name, callback_data=choice_callback_data.new(
        continent=name
    )))

start_menu = InlineKeyboardMarkup()
start_menu.insert(InlineKeyboardButton(text="Начать тест ✏", callback_data="start_question"))
start_menu.insert(InlineKeyboardButton(text="Назад ⬅", callback_data="back"))

next_menu = InlineKeyboardMarkup()
next_menu.insert(InlineKeyboardButton(text="Дальше ➡", callback_data="next_question"))


async def create_question_menu(country, countries):
    question_menu = InlineKeyboardMarkup()

    capital = countries[country]
    capitals = []

    for country in random.sample(list(countries.keys()), 2):
        capitals.append(countries[country])

    capitals.append(capital)

    random.shuffle(capitals)

    for variant in capitals:
        if variant == capital:
            question_menu.add(InlineKeyboardButton(text=variant, callback_data=question_callback_data.new(
                type="correct", capital=variant
            )))
        else:
            question_menu.add(InlineKeyboardButton(text=variant, callback_data=question_callback_data.new(
                type="incorrect", capital=variant
            )))

    return question_menu

