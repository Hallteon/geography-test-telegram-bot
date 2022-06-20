from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter

from states import Test


class IsInStatesGroup(BoundFilter):

    async def check(self, callback: types.CallbackQuery, state: FSMContext):
        return state in Test.all_states[1:]



