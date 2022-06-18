from aiogram.types import InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.inline_keyboards import main_menu, choice_menu, start_menu
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

    start_callback_data = CallbackData("choice_continent", "continent")

    start_menu.insert(InlineKeyboardButton(text="Начать тест ✏", callback_data="start"))
    start_menu.insert(InlineKeyboardButton(text="Назад ⬅", callback_data="back"))

    await callback.message.edit_text(f"Выбран континент: <b>{name}</b> ⛰")
    await callback.message.edit_reply_markup(reply_markup=start_menu)


@dp.callback_query_handler(text="back")
async def back_to_menu(callback: types.CallbackQuery):
    await choice_continent(callback)

