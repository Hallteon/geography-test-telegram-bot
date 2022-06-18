from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.continents_data import continents_data

data = continents_data

choice_callback_data = CallbackData("choice_continent", "continent")
continents = list(data.keys())

main_menu = InlineKeyboardMarkup()
main_menu.insert(InlineKeyboardButton(text="Выбрать континент 🏔", callback_data="choice"))

choice_menu = InlineKeyboardMarkup()

for name in continents:
    choice_menu.insert(InlineKeyboardButton(text=name, callback_data=choice_callback_data.new(
        continent=name
    )))

start_menu = InlineKeyboardMarkup()
